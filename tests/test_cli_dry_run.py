import unittest
import importlib
import sys
import io
from contextlib import redirect_stdout


class CLIDryRunTest(unittest.TestCase):
    def run_cli(self, args):
        old_argv = sys.argv
        sys.argv = ['cli.py'] + args
        f = io.StringIO()
        try:
            # force reload of cli module to ensure argparse picks up sys.argv
            try:
                import cli
                importlib.reload(cli)
            except Exception:
                # module not loaded previously
                import cli
            with redirect_stdout(f):
                try:
                    cli.main()
                except SystemExit:
                    # main may call sys.exit; capture and continue
                    pass
        finally:
            sys.argv = old_argv
        return f.getvalue()

    def test_market_order_dry_run(self):
        out = self.run_cli(['--symbol', 'BTCUSDT', '--side', 'BUY', '--type', 'MARKET', '--quantity', '0.001', '--dry-run'])
        self.assertIn('ORDER REQUEST SUMMARY', out)
        self.assertIn('ORDER EXECUTED SUCCESSFULLY', out)
        self.assertIn('Order ID', out)

    def test_limit_order_dry_run(self):
        out = self.run_cli(['--symbol', 'ETHUSDT', '--side', 'SELL', '--type', 'LIMIT', '--quantity', '0.01', '--price', '3000', '--dry-run'])
        self.assertIn('Price: 3000', out)
        self.assertIn('ORDER EXECUTED SUCCESSFULLY', out)


if __name__ == '__main__':
    unittest.main()
