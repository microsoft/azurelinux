# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import logging
import grpc
import signal
import argparse
from concurrent import futures
from typing import Dict, Any, List, Optional

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace import SpanContext, TraceFlags, TraceState
from opentelemetry.proto.collector.trace.v1 import (
    trace_service_pb2,
    trace_service_pb2_grpc,
)
from opentelemetry.proto.trace.v1.trace_pb2 import Span as ProtoSpan
from opentelemetry.proto.common.v1.common_pb2 import KeyValue

SHUTDOWN_GRACE_PERIOD_SEC = 5

AZURE_CONN_STR = os.getenv("AZURE_MONITOR_CONNECTION_STRING")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("image-customizer-telemetry")


class SpanData:
    """SpanData class for Azure Monitor export."""

    def __init__(
        self, proto_span: ProtoSpan, resource_attrs: Dict[str, Any], inst_scope: Any
    ) -> None:
        try:
            self.name = proto_span.name
            self.start_time = proto_span.start_time_unix_nano
            self.end_time = proto_span.end_time_unix_nano
            self.kind = proto_span.kind

            self.attributes = self._set_attributes(
                proto_span.attributes, resource_attrs
            )
            self.status = self._extract_status(proto_span)

            self.events = self._process_events(proto_span.events)
            self.links = proto_span.links
            self.context = self._create_span_context(
                proto_span.trace_id, proto_span.span_id
            )
            self.parent = self._create_span_context(
                proto_span.trace_id, proto_span.parent_span_id
            )
            self.resource = Resource.create(resource_attrs)
            self.instrumentation_scope = inst_scope

        except Exception as e:
            logger.error(f"Failed to initialize SpanData: {e}")
            raise

    def _process_events(self, proto_events):
        processed_events = []
        for event in proto_events:
            processed_events.append(EventData(event))
        return processed_events

    def _set_attributes(
        self, proto_attributes: List[KeyValue], resource_attrs: Dict[str, Any]
    ) -> Dict[str, Any]:
        attributes = dict(resource_attrs)

        span_attrs = extract_attributes_from_proto(proto_attributes)
        attributes.update(span_attrs)

        return attributes

    def _extract_status(self, proto_span: ProtoSpan) -> Status:
        if proto_span.HasField("status"):
            return Status(
                status_code=StatusCode(proto_span.status.code),
                description=proto_span.status.message or None,
            )
        return Status(StatusCode.UNSET)

    def _create_span_context(self, trace_id, span_id) -> SpanContext:
        return SpanContext(
            trace_id=int.from_bytes(trace_id, "big"),
            span_id=int.from_bytes(span_id, "big"),
            is_remote=True,
            trace_flags=TraceFlags(0),
            trace_state=TraceState(),
        )


class EventData:
    def __init__(self, proto_event):
        self.timestamp = proto_event.time_unix_nano
        self.name = proto_event.name
        self.attributes = extract_attributes_from_proto(proto_event.attributes)


class TraceServiceHandler(trace_service_pb2_grpc.TraceServiceServicer):
    """OTLP trace service handler that forwards traces to Azure Monitor."""

    def __init__(self) -> None:
        """Initialize the trace service handler."""
        self.exporter = self._initialize_telemetry()

    def _initialize_telemetry(self) -> AzureMonitorTraceExporter:
        """Initialize OpenTelemetry and Azure Monitor exporter."""
        provider = TracerProvider(resource=Resource.create({}))
        trace.set_tracer_provider(provider)

        return AzureMonitorTraceExporter(connection_string=AZURE_CONN_STR)

    def Export(self, request, context) -> trace_service_pb2.ExportTraceServiceResponse:
        """Export traces to Azure Monitor."""
        try:
            spans = self._create_spans(request)
            if spans:
                result = self.exporter.export(spans)
                logger.info(
                    "Successfully exported %d spans to Azure Monitor (result: %s)",
                    len(spans),
                    result,
                )
            return trace_service_pb2.ExportTraceServiceResponse()

        except Exception as e:
            logger.error("Error processing spans: %s", e, exc_info=True)
            context.abort(
                grpc.StatusCode.INTERNAL, f"Failed to process spans: {str(e)}"
            )

    def _create_spans(self, request) -> List[SpanData]:
        """Process trace request and convert to SpanData objects."""
        spans = []

        for rs in request.resource_spans:
            resource_attrs = extract_attributes_from_proto(rs.resource.attributes)

            for ss in rs.scope_spans:
                for proto_span in ss.spans:
                    try:
                        span_data = SpanData(proto_span, resource_attrs, ss.scope)
                        spans.append(span_data)
                    except Exception as e:
                        logger.warning(f"Failed to process span {proto_span.name}: {e}")

        return spans


# Utility functions for protobuf attribute extraction
def extract_attribute_value(value_proto: Any) -> Optional[Any]:
    """Extract value from protobuf AnyValue."""
    value_case = value_proto.WhichOneof("value")
    value_mapping = {
        "string_value": value_proto.string_value,
        "int_value": value_proto.int_value,
        "double_value": value_proto.double_value,
        "bool_value": value_proto.bool_value,
    }
    return value_mapping.get(value_case)


def extract_attributes_from_proto(proto_attributes: List[KeyValue]) -> Dict[str, Any]:
    """Extract attributes from protobuf KeyValue pairs."""
    attributes = {}
    for kv in proto_attributes:
        value = extract_attribute_value(kv.value)
        if value is not None:
            attributes[kv.key] = value
    return attributes


class TelemetryServer:
    """Telemetry hopper server that forwards OTLP traces to Azure Monitor."""

    def __init__(self, port: int):
        self.port = port
        self.server: Optional[grpc.Server] = None

    def _start(self) -> None:
        """Start the telemetry forwarding server."""
        try:
            self.server = self._create_server()
            self._setup_signal_handlers()

            self.server.start()
            logger.info(
                f"Telemetry server listening on port {self.port} for OTLP traces"
            )

        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise

    def stop(self, grace_period: int = SHUTDOWN_GRACE_PERIOD_SEC) -> None:
        """Stop the telemetry server gracefully."""
        self.server.stop(grace_period)
        logger.info("Server stopped")

    def wait_for_termination(self) -> None:
        self.server.wait_for_termination()

    def run(self) -> None:
        self._start()
        self.wait_for_termination()

    def _create_server(self) -> grpc.Server:
        server = grpc.server(futures.ThreadPoolExecutor())
        trace_service_pb2_grpc.add_TraceServiceServicer_to_server(
            TraceServiceHandler(), server
        )
        server.add_insecure_port(f"[::]:{self.port}")
        return server

    def _setup_signal_handlers(self) -> None:

        def shutdown_handler(signum, frame):
            logger.info(f"Received signal {signum}, stopping server")
            self.stop()

        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Telemetry hopper server that forwards OTLP traces to Azure Monitor"
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help=f"Port number for the gRPC server to listen on",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    server = TelemetryServer(port=args.port)
    server.run()
