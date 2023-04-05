
## How to

```bash
cd climate-models
source Environment/bin/activate
python3 webapp.py
tailscale server https / http://localhost:5000
tailscale funnel 443 on
```

## Resources
https://tailscale.com/blog/tailscale-funnel-beta/

