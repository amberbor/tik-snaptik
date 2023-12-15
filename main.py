import urllib.request

local_path = "downloaded_image_urllib.jpg"

image_url = "https://p16-sign-va.tiktokcdn.com/tos-maliva-i-photomode-us/9c3fd5a862674f9a995d67bd992ec5f5~tplv-photomode-image.jpeg?from=photomode.AWEME_DETAIL&x-expires=1702774800&x-signature=HAzuKH0JFd1u2DKckdL%2BV7iaR5A%3D"

urllib.request.urlretrieve(image_url, local_path)

