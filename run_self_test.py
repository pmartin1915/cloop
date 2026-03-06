"""
Run Ultrathink self-test suite.
Usage: python run_self_test.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ultrathink.framework import Ultrathink
from ultrathink.self_test import SelfTester, AIErrorDetector


async def main():
    """Run self-test suite."""
    print("\n🧠 Ultrathink Self-Test Suite")
    print("=" * 60)
    print("Testing all components...\n")
    
    # Initialize
    ultrathink = Ultrathink("ultrathink.yaml")
    tester = SelfTester(ultrathink)
    
    # Run tests
    results = await tester.run_full_test_suite()
    
    # Generate report
    report = tester.generate_test_report(results)
    print(report)
    
    # Health check
    print("\n🏥 Running Health Check...")
    detector = AIErrorDetector(ultrathink)
    health = await detector.monitor_health()
    
    print(f"\nSystem Status: {health['status'].upper()}")
    for check_name, check_result in health['checks'].items():
        status = "✓" if check_result['healthy'] else "✗"
        print(f"  {status} {check_name}: {check_result['message']}")
    
    # Exit code
    sys.exit(0 if results['tests_failed'] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
