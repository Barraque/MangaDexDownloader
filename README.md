# MangaDexDownloader

MangaDexDownloader is a tiny program that download your favorite scan from the their website.

## Installation

Use the setup.sh that use [pip](https://pip.pypa.io/en/stable/) to install the different dependencies.

```bash
bash ./setup.sh
```

## Usage

Find the **TitleId** in the list of information about manga requested on the Mangadex website (or in the url, for example : "https://mangadex.org/title/607/berserk" = **607**) .

Then, use it with the list of options below. The default language option is "English" (because ... yes).

getmanga.py [options]

```
Options:
  -h, --help            show this help message and exit
  -i ID, --id=ID        the id of the mangaDex manga
  -b RANGE_MIN, --range_min=RANGE_MIN
                        Begining of the chapter to download (an int)
  -e RANGE_MAX, --range_max=RANGE_MAX
                        End of the chapter to download (an int)
  -l LANGUAGE, --language=LANGUAGE
                        language of the scan
  -L, --show_language   show the list of languages that works on MangaDex

```
## Example
To download Berserk scans for the chapter 6 to the 8 in French:
```bash
python3 getmanga.py -i 607 -b 6 -e 8 -l French
```
To download Berserk scans from the chapter 6:
```bash
python3 getmanga.py -i 607 -b 6
```
To download Berserk scans until the chapter 8:
```bash
./getmanga.py -i 607 -b 6 -e 8
```

Sometimes there is a connection that is refused after a moment. Don't worry re-launch with the **-b** option set as the last unfinished chapter download.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Unlicense](https://choosealicense.com/licenses/unlicense/)
