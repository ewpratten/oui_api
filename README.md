# OUI-API

OUI-API is a very simple REST api for querying company information off their [Organizationally Unique Identifier](https://en.wikipedia.org/wiki/Organizationally_unique_identifier).

## Usage

Send a request to `https://oui.apis.retrylife.ca/lookup/<oui>` to get information on an organization. Example:

```js
// https://oui.apis.retrylife.ca/lookup/000C87
{
    "success": true,
    "vendor":{
        "address": "4555 Great America Pkwy\n Santa Clara CA 95054\n US",
        "company_id": "000C87",
        "organization": "AMD",
        "oui": "00-0C-87"
    }
}
```
