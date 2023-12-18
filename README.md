# And the World Didn't End

Archive for past publications and repo for code aspects of the zine.

Read [the foreword](./zine_pages/md/foreword.md) for more information.

## Archival
TODO Update this section once archival starts

## File structure
Pages should be uploaded in markdown format to [the markdown folder](./zine_pages/md/). [The parser](./zine_parser.py) needs [a little configuring](#configuring-the-parser) but should do the rest for you - creating html files for epub in [./zine_pages/html](./zine_pages/html/) and individual pdf pages in [./zine_pages/pdf/single_pages](./zine_pages/pdf/single_pages/). The full pdf and full pages are generated for publication in 8.5" by 5.5" paper to be printed, and are generated in [./zine_pages/pdf/](./zine_pages/pdf/) for the full zine and [./zine_pages/pdf/full_pages/](./zine_pages/pdf/full_pages/) for individual pages.

### Configuring the parser
The page order is contained in [the corresponding json file](./page_order.json). The file should contain an list called `order` which contains the data. An example is as follows:

```json
{
    "order": [
        "name_of_front_cover",
        "name_of_page_1",
        "name_of_page_2",
        "name_of_back_cover"
    ]
}
```