# MusicDB


## Implemented

- Customized model permissions
- Expiring auth token
- Unit tests
- Custom serializer fields


## API Endpoints

Standard Default Router <a href="http://www.django-rest-framework.org/api-guide/routers/#defaultrouter/">endpoints</a>, plus 

> \/musicians\/free\/ - Musicians who are not in any band

> \/bands\/{pk}\/musicians - Musicians belonging to the band

> \/bands\/{pk}\/albums - Band's albums
