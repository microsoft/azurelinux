#!/bin/bash
# Copyright 2013-2015 Tomas Popela <tpopela@redhat.com>
# Copyright 2022-2024 Than Ngo <than@redhat.com>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# $1 files
# $2 verbose
function copy_files() {
	for file in $1
	do
		dir_name=$(echo "$file" | sed 's%/[^/]*$%/%')
		if [[ $dir_name == */* ]]; then
			tmp_dir_name="tmp_"$dir_name
			mkdir -p "../tmp_ffmpeg/$tmp_dir_name"
		else
			tmp_dir_name=$file
		fi

		if [ "$2" -eq 1 ]; then
			cp "$file" "../tmp_ffmpeg/$tmp_dir_name"
		else
			cp "$file" "../tmp_ffmpeg/$tmp_dir_name" > /dev/null 2>&1
		fi
	done
}

where=$(pwd)

pushd $1
patch -p0 < ../ffmpeg-clean.patch
popd

if ! generated_files=$(./get_free_ffmpeg_source_files.py "$1" "$2"); then
	exit 1
fi
# As the build system files does not contain the header files, cheat here
# and generate the header files names from source files. These that does not
# exist will be later skipped while copying.
generated_files_headers="${generated_files//.c/.h}"
generated_files_headers="$generated_files_headers ${generated_files//.c/_internal.h}"
if [ "$2" -ne "1" ]; then
	generated_files_headers="$generated_files_headers ${generated_files//.S/.h}"
fi
generated_files_headers="$generated_files_headers ${generated_files//.asm/.h}"

header_files="	libavcodec/x86/inline_asm.h \
		libavcodec/x86/hpeldsp.h \
		libavcodec/x86/mathops.h \
		libavcodec/x86/vpx_arith.h \
		libavcodec/aarch64/vp8dsp.h \
		libavcodec/arm/vp8dsp.h \
		libavcodec/arm/vpx_arith.h \
		libavcodec/aac.h \
		libavcodec/aacps.h \
		libavcodec/aacpsdsp.h \
		libavcodec/aacsbrdata.h \
		libavcodec/aac_ac3_parser.h \
		libavcodec/parser.h \
		libavcodec/aac_defines.h \
		libavcodec/ac3.h \
		libavcodec/ac3defs.h \
		libavcodec/ac3tab.h \
		libavcodec/adts_header.h \
		libavcodec/avcodec.h \
		libavcodec/blockdsp.h \
		libavcodec/bytestream.h \
		libavcodec/cbrt_data.h \
		libavcodec/cbrt_tablegen.h \
		libavcodec/codec.h \
		libavcodec/codec_id.h \
		libavcodec/codec_internal.h \
		libavcodec/codec_par.h \
		libavcodec/dct.h \
		libavcodec/dct32.h \
		libavcodec/defs.h \
		libavcodec/dv.h \
		libavcodec/error_resilience.h \
		libavcodec/fdctdsp.h \
		libavcodec/flac.h \
		libavcodec/flacdsp.h \
		libavcodec/flac_parse.h \
		libavcodec/frame_thread_encoder.h \
		libavcodec/get_bits.h \
		libavcodec/h263dsp.h \
		libavcodec/h264chroma.h \
		libavcodec/hevc/hevc.h \
		libavcodec/hpeldsp.h \
		libavcodec/hwaccels.h \
		libavcodec/hwaccel_internal.h \
		libavcodec/hwconfig.h \
		libavcodec/idctdsp.h \
		libavcodec/internal.h \
		libavcodec/itut35.h \
		libavcodec/kbdwin.h \
		libavcodec/mathops.h \
		libavcodec/me_cmp.h \
		libavcodec/mlp_parse.h \
		libavcodec/motion_est.h \
		libavcodec/mpeg12.h \
		libavcodec/mpeg12data.h \
		libavcodec/mpeg12vlc.h \
		libavcodec/mpegaudio.h \
		libavcodec/mpegaudiodecheader.h \
		libavcodec/mpegaudiodec_common_tablegen.h \
		libavcodec/mpegaudiodsp.h \
		libavcodec/mpegaudio_tablegen.h \
		libavcodec/mpegpicture.h \
		libavcodec/mpegutils.h \
		libavcodec/mpegvideo.h \
		libavcodec/mpegvideodata.h \
		libavcodec/mpegvideoencdsp.h \
		libavcodec/opus/enc.h \
		libavcodec/opus/opus.h \
		libavcodec/options_table.h \
		libavcodec/packet.h \
		libavcodec/packet_internal.h \
		libavcodec/pcm_tablegen.h \
		libavcodec/pixblockdsp.h \
		libavcodec/pixels.h \
		libavcodec/png.h \
		libavcodec/pngdsp.h \
		libavcodec/progressframe.h \
		libavcodec/put_bits.h \
		libavcodec/qpeldsp.h \
		libavcodec/ratecontrol.h \
		libavcodec/rectangle.h \
		libavcodec/rl.h \
		libavcodec/rnd_avg.h \
		libavcodec/sbr.h \
		libavcodec/sbrdsp.h \
		libavcodec/sinewin.h \
		libavcodec/sinewin_tablegen.h \
		libavcodec/startcode.h \
		libavcodec/thread.h \
		libavcodec/threadframe.h \
		libavcodec/unary.h \
		libavcodec/version.h \
		libavcodec/version_major.h \
		libavcodec/videodsp.h \
		libavcodec/vlc.h \
		libavcodec/vorbisdsp.h \
		libavcodec/vp3data.h \
		libavcodec/vp4data.h \
		libavcodec/vp3dsp.h \
		libavcodec/vp56.h \
		libavcodec/vp56dsp.h \
		libavcodec/vp8data.h \
		libavcodec/vp8dsp.h \
		libavcodec/vp89_rac.h \
		libavformat/apetag.h \
		libavformat/avformat.h \
		libavformat/dv.h \
		libavformat/img2.h \
		libavformat/internal.h \
		libavformat/mov_chan.h \
		libavformat/pcm.h \
		libavformat/rdt.h \
		libavformat/rtp.h \
		libavformat/rtpdec.h \
		libavformat/spdif.h \
		libavformat/srtp.h \
		libavformat/options_table.h \
		libavformat/version.h \
		libavformat/version_major.h \
		libavformat/w64.h \
		libavformat/iamf_parse.h \
		libavformat/iamf_reader.h \
		libavformat/iamf.h \
		libavformat/dvdclut.h \
		libavutil/aarch64/cpu.h \
		libavutil/aarch64/intreadwrite.h \
		libavutil/x86/asm.h \
		libavutil/x86/bswap.h \
		libavutil/x86/cpu.h \
		libavutil/emms.h \
		libavutil/x86/intreadwrite.h \
		libavutil/x86/intmath.h
		libavutil/x86/timer.h \
		libavutil/attributes.h \
		libavutil/attributes_internal.h \
		libavutil/audio_fifo.h \
		libavutil/avassert.h \
		libavutil/avutil.h \
		libavutil/bswap.h \
		libavutil/common.h \
		libavutil/colorspace.h \
		libavutil/cpu.h \
		libavutil/cpu_internal.h \
		libavutil/dynarray.h \
		libavutil/ffmath.h \
		libavutil/fixed_dsp.h \
		libavutil/float_dsp.h \
		libavutil/imgutils.h \
		libavutil/imgutils_internal.h \
		libavutil/internal.h \
		libavutil/intfloat.h \
		libavutil/intreadwrite.h \
		libavutil/libm.h \
		libavutil/lls.h \
		libavutil/macros.h \
		libavutil/pixfmt.h \
		libavutil/qsort.h \
		libavutil/replaygain.h \
		libavutil/softfloat.h \
		libavutil/softfloat_tables.h \
		libavutil/thread.h \
		libavutil/timer.h \
		libavutil/timestamp.h \
		libavutil/tx_priv.h \
		libavutil/version.h \
		libavutil/sfc64.h \
		libavutil/executor.h \
		libswresample/swresample.h \
		libswresample/version.h \
		libswresample/version_major.h \
		compat/va_copy.h "

manual_files=" libavcodec/aarch64/h264pred_neon.S \
		libavcodec/aarch64/hpeldsp_neon.S \
		libavcodec/aarch64/neon.S \
		libavcodec/aarch64/vorbisdsp_neon.S \
		libavcodec/aarch64/autorename_libavcodec_aarch64_vorbisdsp_neon.S \
		libavcodec/aarch64/autorename_libavcodec_aarch64_vorbisdsp_init.c \
		libavcodec/aarch64/autorename_libavcodec_aarch64_videodsp_init.c \
		libavcodec/aarch64/vorbisdsp_init.c \
		libavcodec/aarch64/vp8dsp_neon.S \
		libavcodec/x86/hpeldsp.asm \
		libavcodec/x86/hpeldsp_rnd_template.c \
		libavcodec/x86/rnd_template.c \
		libavcodec/x86/videodsp.asm \
		libavcodec/x86/videodsp_init.c \
		libavcodec/x86/vorbisdsp_init.c \
		libavcodec/x86/vp3dsp.asm \
		libavcodec/x86/vp8dsp.asm \
		libavcodec/bit_depth_template.c \
		libavcodec/flacdec.c \
		libavcodec/flacdsp.c \
		libavcodec/flacdsp_template.c \
		libavcodec/flacdsp_lpc_template.c \
		libavcodec/h264pred_template.c \
		libavcodec/hpel_template.c \
		libavcodec/hpeldsp.c \
		libavcodec/options.c \
		libavcodec/parser.c \
		libavcodec/pcm.c \
		libavcodec/pel_template.c \
		libavcodec/utils.c \
		libavcodec/videodsp.c \
		libavcodec/videodsp_template.c \
		libavcodec/vorbisdsp.c \
		libavcodec/vp3dsp.c \
		libavcodec/vp8dsp.c \
		libavformat/flacdec.c \
		libavformat/options.c \
		libavformat/pcm.c \
		libavformat/utils.c \
		libavformat/version.c \
		libavformat/dvdclut.c \
		libavutil/aarch64/asm.S \
		libavutil/aarch64/cpu.c \
		libavutil/aarch64/cpu_sve.S \
		libavutil/aarch64/float_dsp_init.c \
		libavutil/aarch64/float_dsp_neon.S \
		libavutil/aarch64/autorename_libavutil_aarch64_cpu.c \
		libavutil/aarch64/autorename_libavutil_aarch64_float_dsp_init.c \
		libavutil/aarch64/autorename_libavutil_aarch64_float_dsp_neon.S \
		libavutil/aarch64/tx_float_neon.S \
		libavutil/aarch64/timer.h \
		libavutil/cpu.c \
		libavutil/fixed_dsp.c \
		libavutil/float_dsp.c \
		libavutil/imgutils.c \
		libavutil/tx_float.c \
		libavutil/tx_template.c \
		libavutil/utils.c \
		libavutil/version.c \
		libavutil/x86/cpu.c \
		libavutil/x86/float_dsp_init.c \
		libavutil/x86/tx_float_init.c \
		libavutil/aarch64/tx_float_init.c \
		libavutil/executor.c \
		libavutil/x86/x86inc.asm \
		libavutil/x86/x86util.asm "

mp3_files="	libavcodec/aarch64/aacpsdsp_init_aarch64.c \
		libavcodec/aarch64/aacpsdsp_neon.S \
		libavcodec/aarch64/autorename_libavcodec_aarch64_aacpsdsp_neon.S \
		libavcodec/aarch64/autorename_libavcodec_aarch64_sbrdsp_neon.S \
		libavcodec/aarch64/mpegaudiodsp_init.c \
		libavcodec/aarch64/mpegaudiodsp_neon.S \
		libavcodec/aarch64/sbrdsp_init_aarch64.c \
		libavcodec/aarch64/sbrdsp_neon.S \
		libavcodec/aac_ac3_parser.c \
		libavcodec/aac_parser.c \
		libavcodec/aacps_float.c \
		libavcodec/aacpsdsp_float.c \
		libavcodec/aacsbr.c \
		libavcodec/aactab.c \
		libavcodec/ac3tab.c \
		libavcodec/autorename_libavcodec_mpegaudiodsp.c \
		libavcodec/autorename_libavcodec_sbrdsp.c \
		libavcodec/cbrt_data.c \
		libavcodec/dct32_fixed.c \
		libavcodec/dct32_float.c \
		libavcodec/dct32_template.c \
		libavcodec/kbdwin.c \
		libavcodec/mpegaudio.c \
		libavcodec/mpegaudio_parser.c \
		libavcodec/mpegaudiodec_fixed.c \
		libavcodec/mpegaudiodec_template.c \
		libavcodec/mpegaudiodecheader.c \
		libavcodec/mpegaudiodsp.c \
		libavcodec/mpegaudiodsp_data.c \
		libavcodec/mpegaudiodsp_fixed.c \
		libavcodec/mpegaudiodsp_float.c \
		libavcodec/mpegaudiodsp_template.c \
		libavcodec/sbrdsp.c \
		libavcodec/sbrdsp_template.c \
		libavcodec/sinewin.c \
		libavcodec/x86/dct32.asm \
		libavcodec/x86/imdct36.asm \
		libavcodec/x86/mpegaudiodsp.c \
		libavcodec/x86/sbrdsp_init.c \
		libavcodec/x86/sbrdsp.asm \
		libavformat/aacdec.c \
		libavformat/apetag.c \
		libavformat/img2.c \
		libavformat/mov.c \
		libavformat/mov_chan.c \
		libavformat/mp3dec.c "

other_files="	BUILD.gn \
		Changelog \
		COPYING.GPLv2 \
		COPYING.GPLv3 \
		COPYING.LGPLv2.1 \
		COPYING.LGPLv3 \
		CREDITS \
		CREDITS.chromium \
		ffmpeg_generated.gni \
		ffmpeg_options.gni \
		INSTALL.md \
		LICENSE.md \
		MAINTAINERS \
		OWNERS \
		README.chromium \
		README.md \
		RELEASE "

cd "$1/third_party/ffmpeg" || exit 1

copy_files "$generated_files" 0
copy_files "$generated_files_headers" 0
copy_files "$manual_files" 1
copy_files "$other_files" 1
copy_files "$header_files" 1
copy_files "$mp3_files" 1

mkdir -p ../tmp_ffmpeg/tmp_chromium/config
cp -r chromium/config ../tmp_ffmpeg/tmp_chromium

cd ../tmp_ffmpeg || exit 1

while IFS= read -r -d '' tmp_directory
do
	new_name=${tmp_directory//tmp_/}
	mv "$tmp_directory" "$new_name"
done <  <(find . -type d -name 'tmp_*' -print0)

cd "$where" || exit 1

rm -rf "$1/third_party/ffmpeg"
mv "$1/third_party/tmp_ffmpeg" "$1/third_party/ffmpeg"
