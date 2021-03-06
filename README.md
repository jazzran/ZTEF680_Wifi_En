# ZTEF680_Wifi_En

Python tool for enabling and disabling WIFI remotely in ZTE F680 routers.

Python3 & 2 supported

## Execution example

```
./wifichange.py -p testPass -e 1 -t 2 -u 1234 -i 192.168.0.1
```
This modifies the configuration in router _192.168.0.1_ with user _1234_ and password _testPass_ enabling (_-e 1_) 5G wifi (_-t 2_)

## How it works
1. Obtain LoginToken for doing authentication
2. Generate Hash and random value for authentication
3. Using loginToken obtains SID cookie value
4. Obtain session Token for being able to operate
5. Enable/Disable WIFI
6. Logout


## Known limitations
Wifi parameters are Hardcoded. Default settings: Spain Bands. If you need to update it with your settings you need to edit the ZTE.py file

## Future evolutions

~~Migrate to Python3~~

Extract settings to only one centralized point.

Obtain WIFI configured parameters from router instead of using Harcoded ones 

## Contributing

Please read [CONTRIBUTING.md](https://github.com/jazzran/ZTEF680_Wifi_En/blob/master/Contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.
