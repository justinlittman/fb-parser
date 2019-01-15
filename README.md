# fb-parser
Parses posts from Facebook pages recorded in WARC files and outputs as CSV.

*This project is experimental.*

## Setup

```
git clone https://github.com/justinlittman/fb-parser.git
cd fb-parser
pip install -r requirements.txt

```

## Use
1. Use WebRecorder to record a Facebook page and download the WARC file. See [these instructions](docs/recording.md).

2. Run fb-parser. For example:

```
python fb_parser.py sample-20190114025817.warc > sample-20190114025817.csv
```

`sample-20190114025817.warc` is included so that you can try fb-parser.

Here is a sample of the output:
```
January 9 at 5:37 PM,A lot of Virginia miners and their families are counting on the healthcare and pension benefits they earned through years of hard work. I’m sponsoring the American Miners Act with Senator Joe Manchin III and U.S. Senator Tim Kaine to protect those benefits.
January 4 at 12:46 PM,"Today I’m joining Senator Joe Manchin III and U.S. Senator Tim Kaine in introducing the American Miners Act, which will protect healthcare and pensions for retired miners and shore up the Black Lung Disability Trust Fund. The federal government made a promise to miners and their families, and we intend to keep it."
January 8 at 9:32 PM,Nothing we heard tonight justifies shutting down the government and throwing the lives of thousands of federal workers and contractors into chaos. It's time for the President to reopen the government.
```

## How it works
Facebook pages use XHR to transfer data about posts for rendering on the page. WebRecorder records each of the
XHR requests and responses in the WARC file. fb-parser parses the post data from the XHR payloads contained in the WARC file.
