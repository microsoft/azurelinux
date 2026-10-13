<?php declare(strict_types=1);

namespace SebastianBergmann\CodeCoverage\Util;

use function preg_match;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Small;
use PHPUnit\Framework\TestCase;
use ReflectionClass;

final class PhpParserVersionRPMTest extends TestCase
{
    public function testVersion(): void
    {
        $version = PhpParserVersion::id();

        $this->assertNotSame('unknown', $version);
        $this->assertTrue(preg_match('/^5\.[0-9]+\.[0-9]+/', $version) === 1);
        $this->assertTrue(PhpParserVersion::isExact());
    }

}
