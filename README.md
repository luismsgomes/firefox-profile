# Firefox profile

Copyright 2020 Luís Gomes <luismsgomes@gmail.com>, all rights reserved.


## Installation

    pip3 install firefox-profile

## Usage from Python


    from firefox_profile import FirefoxProfile

    for profile in FirefoxProfile.get_profiles():
        recovery_data = profile.get_recovery_data()
        if recovery_data is None:
            continue
        for i, window in enumerate(recovery_data.windows):
            # do something with window:
            print(f"window {i}")
            print(f"  workspace: {window.workspace}")
            print(f"  zindex: {window.zindex}")
            print(f"  size: {window.size!r}")
            print(f"  position: {window.position!r}")
            print(f"  mode: {window.mode}")
            print(f"  tabs:")
            for j, tab in enumerate(window.tabs):
                # do something with tab:
                print(f"    tab {j}")
                print(f"      url: {tab.url}")
                print(f"      title: {tab.title}")
                print(f"      last_accessed: {tab.last_accessed}")


## Usage from command line

    firefox-profile-json

Will output something like:

    [
        {
            "profile": "default",
            "windows": [
                {
                    "tabs": [
                        {
                            "last_accessed": "2020-12-07T17:16:19.703000",
                            "url": "https://docs.python.org/3/library/os.html#os.open",
                            "title": "os \u2014 Miscellaneous operating system interfaces \u2014 Python 3.9.1rc1 documentation"
                        }
                    ]
                }
            ],
            "workspace": "2",
            "zindex": 3,
            "size": [
                1716,
                1373
            ],
            "position": [
                0,
                37
            ],
            "mode": "minimized"
        }
    ]


## License

This software is licensed under the MIT license.

https://opensource.org/licenses/MIT
