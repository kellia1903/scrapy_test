BOT_NAME = "test_apteka_ot_sklada"

SPIDER_MODULES = ["test_apteka_ot_sklada.spiders"]
NEWSPIDER_MODULE = "test_apteka_ot_sklada.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    'result_%(time)s.json': {'format': 'json',
                             'overwrite': True,}
}