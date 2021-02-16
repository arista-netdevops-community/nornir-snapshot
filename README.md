# How to use nornir-snapshot

1. Clone this repository.
2. Review `config.yaml`. Normally there is no need to adjust it, but you may check number of workers running at once.
3. Adjust `defaults.yaml` with the correct login and password. NOTE: this is not secure. Do not push this commit to any git repositories except your local machine. Or check Nornir documentation for secure storage options.
4. Review `groups.yaml`. For a basic case it can be used as is. But adjusting groups and parameters may be required if not covering your specific case.
5. Edit the inventory in the `hosts.yaml`.
6. Create Python3 virtual environment with `python3 -m venv .venv`. Activate it if not activated by IDE automatically: `source .venv/bin/activate`
7. Upgrade pip: `pip install --upgrade pip`
8. Install requirements: `pip install -r requirements.txt`
