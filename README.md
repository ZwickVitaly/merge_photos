# Merge photos microservice

### Description:
Starts a microservice with one active path:
```
POST [hostname]/make-tiff
```
with json-body, containing link to public yandex-disk and some params.\
Goes recursively through this disk, downloading all found images,\
sorting them to lists by directory, and then merging them to single\
.tiff collection. One folder = one page. On page images are merged into\
grid of equal-sized images.\
Docs how to use and parameters description (swagger) are available on
```commandline
GET [hostname]/docs
```
### Installation:
Assuming you have docker installed:
```commandline
docker compose up --build -d
```
That's all, service is ready to go. 
### Addition:
TiffMaker class (app/utils/tiffmaker.py) is fully usable outside of main app.\
TiffMaker.make_tiff() accepts links(ye ye I'll rename it later): list[PIL.Image] and filename: str\
Will merge list of images and save it to filename on disk.\
If you need to save merge .tiff to memory - rewrite method, have fun.
# That's all, folks
