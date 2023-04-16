from ..constants import extra_characters, volume_units


def title_convert(response):
    """Функция преобразования заголовка товара."""
    title = response.xpath('//h1/span/text()').get()
    data = []
    volume = ''
    amount = ''
    for unit in volume_units:
        index_unit = title.rfind(unit)
        if index_unit != -1:
            for symbol in title[(index_unit - 5): index_unit]:
                if symbol.isdigit():
                    volume += symbol
            volume += ' ' + unit
            title = title.replace(volume, '')
            title = title.replace(volume.replace(' ', ''), '')
    index_number = title.rfind('N')
    if index_number not in [-1, 0, 1]:
        for symbol in title[index_number::]:
            if symbol.isdigit():
                amount += symbol
        amount += ' шт'
        title = title[:index_number]
    data.append(title)
    if volume != '':
        data.append(volume)
    if amount != '':
        data.append(amount)
    if len(data) == 1:
        return title
    return data


def marketing_tags_convert(response):
    """Функция приведения тэгов к нужному формату."""
    data = []
    tags_no_format = response.xpath(
        '//li[@class="goods-tags__item"]/span/text()'
    ).getall()
    if tags_no_format is not None:
        for tag in tags_no_format:
            data.append(' '.join(tag.split()))
    return data


def price_data_convert(response):
    """Функция преобразования цены."""
    data = {
        "current": 0,
        "original": 0,
        "sale_tag": '',
    }
    prices = response.xpath(
        '//div[@class="goods-offer-panel__price"]//text()'
    ).getall()
    if prices != []:
        current_price = ''.join(
            [x for x in prices[0] if x.isdigit() or x == '.']
        )
        data["current"] = data["original"] = float(current_price)
        if prices[-1] != ' ':
            original_price = ''.join(
                [x for x in prices[-1] if x.isdigit() or x == '.']
            )
            data["original"] = float(original_price)
            sale = data["current"] // data["original"] * 100
            data["sale_tag"] = f'Скидка {sale}%'

    return data


def stock_convert(response):
    """Функция преобразования наличия товара."""
    data = {
        "in_stock": False,
        "count": 0,
    }
    button_on_page = response.xpath(
        '''//div[@class="goods-cart-form"]'''
        '''//span[@class="ui-button__content"]/text()'''
    ).get()
    if button_on_page is not None:
        data["in_stock"] = 'добавить в корзину' in button_on_page.lower()
    return data


def assets_convert(response):
    """Функция преобразования изображений товара."""
    data = {
        "main_image": '',
        "set_images": [],
        "view360": [],
        "video": [],
    }
    images = response.xpath(
        '//div[@class="goods-gallery__sidebar"]//img/@src'
    ).getall()
    if images is not None:
        data["main_image"] = images[0]
        data["set_images"] = images
    return data


def metadata_convert(response):
    """Функция преобразования метаданных."""
    data = {
        "__description": '',
    }
    description = response.xpath(
        '//div[@itemprop="description"]//p/text()'
    ).getall()
    if description is not None:
        for paragraph in description:
            for symbol in extra_characters:
                paragraph = paragraph.replace(symbol, '')
            data["__description"] += paragraph
    specifications = response.xpath(
        '//div[@itemprop="description"]//li/text()'
    ).getall()
    if specifications is not None:
        for specification in specifications:
            try:
                for symbol in extra_characters:
                    specification = specification.replace(symbol, '')
                parametr, value = specification.split(':')
                data[parametr.upper()] = value
            except Exception:
                data["parametr"] = 'Не верный формат данных'
    return data
