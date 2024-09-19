# ignitionExporter
- A OSS data historian for ignition. InfluxDB stores OPCUA data scraped by telegraf. Grafana can be used to visualize the results.


## Testing
### Ignition
- If the ignition container's data is deleted, you need to go to `Config>OPC UA>Server Settings` and set the following settings
    - `Endpoint Configuration>Bind Address:` `0.0.0.0`
    - `Endpoint Configuration>Security Policies:` `None, Basic256Sha256`
    - `Authentication> Anonymous Access Allowed:` `true`
    - `Advanced> Expose Tag Providers:` `true`
- Then, restart the ignition container for these settings to take effect


# TODO
- [ ] Better management of shared env vars
- [ ] Experiment with `input.opcua_listener`
- [ ] Setup and provision grafana
