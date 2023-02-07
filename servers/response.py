import requests


class response:

    def get(url):
        # 请求头
        headers = {
            'connection':
            'keep-alive',
            'sec-ch-ua-platform':
            "macOS",
            'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                return res
            else:
                return ''
        except:
            return ''
