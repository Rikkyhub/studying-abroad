"""Exercise the shipped, self-contained budget page in Chrome on the CI runner."""
import html
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHROME = shutil.which("google-chrome")
# Use an iframe to set an exact mobile viewport regardless of the host window size.
CHECK = """
const frame = document.querySelector('iframe');
frame.onload = () => {
  const doc = frame.contentDocument;
  const dashboard = doc.querySelector('.travel-budget');
  const buttons = dashboard.querySelectorAll('.controls button');
  const expect = (condition, message) => { if (!condition) throw Error(message); };
  const result = document.querySelector('output');
  try {
    expect(buttons.length === 6, 'six controls');
    const total = dashboard.querySelector('[data-total]').textContent;
    for (const button of buttons) {
      button.click();
      expect(button.getAttribute('aria-pressed') === 'true', button.value);
      const groups = dashboard.querySelectorAll('.group');
      expect(groups.length > 0, 'no groups: ' + button.value);
      groups[0].querySelector('summary').click();
      expect(groups[0].open, 'detail closed');
      expect(dashboard.getBoundingClientRect().right <= frame.clientWidth + 1, 'width');
      expect(dashboard.scrollWidth <= dashboard.clientWidth + 1, 'horizontal overflow');
      expect(dashboard.querySelector('[data-total]').textContent === total, 'total changed');
      if (button.value === 'payment') {
        const select = groups[0].querySelector('select');
        select.value = '支払済み';
        select.dispatchEvent(new Event('change'));
        expect(dashboard.querySelector('[data-groups]').textContent.includes('支払済み　'), 'payment group');
      }
      if (button.value === 'months') {
        expect([...groups].some(g=>g.querySelector('summary').textContent.includes('2027-08')), 'August');
      }
    }
    const plan = dashboard.querySelector('[data-plan]');
    const values = {};
    for (const key of ['low', 'high', 'std']) {
      plan.value = key;
      plan.dispatchEvent(new Event('change'));
      values[key] = Number(dashboard.querySelector('[data-total]').textContent.replace(/[^0-9]/g, ''));
    }
    expect(values.low < values.std && values.std < values.high, 'scenario totals');
    expect(dashboard.querySelector('[data-total]').textContent === total, 'restore standard');
    result.textContent = 'PASS';
  } catch(error) { result.textContent = error.message; }
};
"""


@unittest.skipUnless(CHROME and os.environ.get("CI"), "Chrome screen check runs in CI")
class BudgetBrowserTest(unittest.TestCase):
    def test_mobile_and_desktop(self):
        page = (ROOT / "docs/02-budget.html").read_text(encoding="utf8")
        with tempfile.TemporaryDirectory() as tmp:
            wrapper = Path(tmp) / "screen.html"
            for width in (375, 1280):
                with self.subTest(width=width):
                    wrapper.write_text(
                        f'<meta charset="utf-8"><iframe style="width:{width}px;height:850px"></iframe>'
                        f'<output>pending</output><script>{CHECK}</script><template>'
                        + html.escape(page) + '</template><script>document.querySelector("iframe").srcdoc='
                        'document.querySelector("template").content.textContent;</script>', encoding="utf8")
                    run = subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                                          f"--user-data-dir={tmp}/profile-{width}", "--dump-dom",
                                          "--virtual-time-budget=5000", wrapper.as_uri()],
                                         capture_output=True, text=True, timeout=60, check=True)
                    result = run.stdout.partition("<output>")[2].partition("</output>")[0]
                    self.assertEqual(result, "PASS")
