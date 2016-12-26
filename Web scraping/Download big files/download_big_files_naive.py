import requests


def download(url):

    resp = requests.get(url)
    print("Content-Length: {}".format(resp.headers["Content-Length"]))
    return resp.content

if __name__ == '__main__':

    url = "http://github-images.s3.amazonaws.com/blog/2011/cc-wallpaper-desktop.png"
    bs = download(url)

    with open("test_naive.png", "wb") as f:
        f.write(bs)
