# Flask + Nuxt/Vue video streaming template

Upload video -> fragment it using [bento4](https://www.bento4.com/) and save -> return file name

Take file name -> fetch codecs -> stream video using `MediaSource`

----

* [Download bento4](https://www.bento4.com/downloads/)
* Configure `BENTO_DIR` in app.py like this: `back/<BENTO_DIR>/bin/mp4fragment.exe`
* `python3 back/app.py`
`cd front`
`npm i`
`npm run dev`
