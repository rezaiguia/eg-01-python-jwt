import docusign_esign as docusign

from ds_helper import DSHelper
from list_envelopes import ListEnvelopes
from send_envelope import SendEnvelope
from ds_config import DSConfig

def main():
    api_client = docusign.ApiClient()

    CONSENT_REDIRECT_URL = "https://www.docusign.com" # Just used for individual permission request

    try:
        print("\nSending an envelope...")
        result = SendEnvelope(api_client).send_envelope()
        print("Envelope status: {}. Envelope ID: {}".format(result.status, result.envelope_id))

        print("\nList envelopes in the account whose status changed in the last 30 days...")
        envelopes_list = ListEnvelopes(api_client).list()
        envelopes = envelopes_list.envelopes
        num_envelopes = len(envelopes)
        if num_envelopes > 2:
            print("Results for {} envelopes were returned. Showing the first two:\n".format(num_envelopes))
            envelopes_list.envelopes = [envelopes[0], envelopes[1]]
        else:
            print("Results for {} envelopes were returned:\n".format(num_envelopes))

        DSHelper.print_pretty_json(envelopes_list)
    except docusign.rest.ApiException as err:
        print ("\n\nDocuSign Exception!")

        # Special handling for consent_required
        body = err.body.decode('utf8')
        if "consent_required" in body:
            consent_scopes = "signature%20impersonation"
            consent_url = "{}/oauth/auth?response_type=code&scope={}&client_id={}&redirect_uri={}".format(DSConfig.auth_server(), consent_scopes, DSConfig.client_id(), CONSENT_REDIRECT_URL)
            print ("""
\nC O N S E N T   R E Q U I R E D
Ask the user who will be impersonated to run the following url:
    {}

It will ask the user to login and to approve access by your application.

Alternatively, an Administrator can use Organization Administration to
pre-approve one or more users.""".format(consent_url))
        else:
            print ("   Reason: {}".format(err.reason))
            print ("   Error response: {}".format(err.body.decode('utf8')))

    print("\nDone.\n")

if __name__ == "__main__":
    main()
