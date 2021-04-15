import requests
import uuid

class ASOS:
    def __init__(self):
        pass

    def cart():
        s = requests.session()
        cookie = 'EDF8BD26C79045226ACBFC3D0E282E96~-1~YAAQN0YUAgA3A494AQAAUKyUrAUj/RszE10ZzIJW1qS4MPmn0RSlTVSP+43kGdK1UQU699GJkwCOvYvhjWdRuRaopTGYJolrr9nQDYFt4DoQ8nFdTbpvTC8hWHGgUVtWJDjKsdy8Yt20OBaCP3OTkUCt+5IvMuGC2JBwfnE3xDdaFprCXMcRB2RmutMMaXViJvSU3bYUEhtBHxSwaEcHoReowEgnNIPT+TGbVZzWFa9URQAooLF2gcHbmTHqEjlF+RohxONx70b7KhN0dpnESJ253TwcTtJMrWG2ZYRZJ9W5QU8lTxDdYpS1LkjJK1Z5Jy9UQmDkg5DutzszuH1lp47gOrSd4s3llWdsGyFRqhu4kOH3fj2/nHWZ5OT34fzDO6kBhVpZlmY=~-1~-1~-1'
        r = s.post('https://www.asos.com/api/commerce/bag/v4/bags/91c06835-0e66-4efe-bdd1-f5a8bf8c421f/product?expand=summary,total&lang=en-GB',headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "asos-bag-origin": "EUN",
                "asos-c-ismobile": "false",
                "asos-c-istablet": "false",
                "asos-c-name": "Asos.Commerce.Bag.Sdk",
                "asos-c-plat": "Web",
                "asos-c-store": "COM",
                "asos-c-ver": "5.1.0",
                "asos-cid": str(uuid.uuid4()),
                "authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjB6Y3RJdzd2WHdZSGRTT1J1NW5JWnRjajNrQSJ9.eyJpZHAiOiJzaXRlIiwic3ViIjoiMTI3NTExOTM5IiwiYWlkIjoiMzBlZmY4MzAxMGJmNDNkZjk0ODc5YzRjZTg0OWIxNzEiLCJhbXIiOlsiYXNvcyJdLCJmdGIiOmZhbHNlLCJjZ2QiOiJjNWZkNTcyZGUxMzI0NzkyYTBlYThmOTAzNzNhODk5MiIsImlzcyI6Imh0dHBzOi8vbXkuYXNvcy5jb20vdHJ1c3QiLCJhdWQiOiJodHRwczovL2FwaS5hc29zLmNvbSIsImV4cCI6MTYxNzgwNTAwNSwibmJmIjoxNjE3ODAxNDA1LCJzY29wZSI6WyJzZW5zaXRpdmUiXSwic2VzcyI6IjAwYzEyNTkxZmUxMTQxMDA4NWZkZjkzNTBlNjFmZDljIn0.LHPBLQHr8v9cNuSAvEEABx5086BqjbWe0FU-xA8snpMo4HPvOxe3-64VIbebPO2lwd1zCmlmfvpd8FM4d2-X8DpXhAUqTQ-bl0Ca0M3ddtzMpBcVVTLkbzWS3l87RpBt0z4AcdtCaq-9T8cOKUsslc4q7x1gH_KLdNR1WvmKqa1WJWYqNPXUZ1WcGcXKWsjSDskgY-6bDo9FT6ybBQmH-Snjhyj5lBYT-J81Ge-eVsqhoejSxuq_FDGZ-1xjd7fpXDOd01g0OUy05jR0pIa6YBrZhMVKYiL0xhCK15Q7QWcwg626Gi9EYlLKBVeJh6sSxwFSxm2QJZL6r0UrHKtnaRdhjd4F0lGgnp5MSfUtrC0PRRxY91BAXhCNzhSyV5WwMfacysnbah2AB7nPx8DKyS-HQQO8YnA__9BbV8CnYEk-adHhwj77ms8pInSJjM39v9gNfrRkTIOxS1DFkM6ndBFGDMokyAhZF8m-_5W-EWD8PVYR8gPKEjEwp9VN1Q7I6h7CEl7G7TmnurXEZukSZzmEa1fxP4_-zI792Y47R5PWfedRHByVNbRcly6oBJxrWk9PZIdlAdkUV7cjCAWHlyMO91UmVsIGShRdzFLl_mW9IRGkf3c-oabPSgOeRkPhqk4U-hmMRCA4HaVFNqOo6tLL26tZSaEuVY8_rcliQpQ",
                "content-type": "application/json",
                "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                "cookie": f"_abck={cookie};"
            },json={"variantId":22128043})

        print(r)
        print(r.text)


# ASOS.cart()