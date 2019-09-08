import requests


def post(payload):
    '''
    Login the website myportal of De Anza, 'https://ssoshib.fhda.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1'
    using payload.
    Payload is the dictionary of username and password
    '''
    r = requests.post('https://ssoshib.fhda.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1', data=payload)
    #print("cookies:\n", r.cookies.get_dict())
    r = requests.get('https://ssoshib.fhda.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1', cookies=r.cookies)
    #print("text:\n", r.text)


if __name__ == '__main__':
    '''
    using username and password to login the website of myportal
    '''
    payload = {'username': '20256448', 'password': 'Daz2018continue'}
    post(payload)
