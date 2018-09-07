from pyquery import PyQuery as py
import crawl_goubanjia

with_space_html = '<td class="ip"><div style="display: inline-block;">11</div><span style="display: inline-block;">7</span><span style="display: inline-block;"></span><p style="display:none;">.1</p><span>.1</span><div style="display: inline-block;"></div><span style="display: inline-block;"></span><span style="display: inline-block;"></span><p style="display:none;">7</p><span>7</span><p style="display: none;">7.</p><span>7.</span><p style="display: none;"></p><span></span><span style="display: inline-block;">24</span><div style="display: inline-block;">3.</div><span style="display: inline-block;"></span><p style="display: none;">7</p><span>7</span>:<span class="port GEA">80</span></td>'
without_space_html = '<td class="ip"><div style="display:inline-block;">11</div><span style="display:inline-block;">7</span><span style="display:inline-block;"></span><p style="display:none;">.1</p><span>.1</span><div style="display:inline-block;"></div><span style="display:inline-block;"></span><span style="display:inline-block;"></span><p style="display:none;">7</p><span>7</span><p style="display:none;">7.</p><span>7.</span><p style="display:none;"></p><span></span><span style="display:inline-block;">24</span><div style="display:inline-block;">3.</div><span style="display:inline-block;"></span><p style="display:none;">7</p><span>7</span>:<span class="port GEA">80</span></td>'

actual_ip = '117.177.243.7'

def test_get_ip():
    row = py(with_space_html)
    ip1 = crawl_goubanjia.get_ip(row)

    without_space_row = py(without_space_html)
    ip2 = crawl_goubanjia.get_ip(without_space_row)

    assert ip1 == actual_ip
    assert ip2 == actual_ip
