import xlwt
from apps.kiltshop.models import Product, ProductInfo, OrderPeriod


def create_excel(pk):
    """
    Create an excel file containing order data for an entire period
    :param pk: primary key of order period
    :return: an xlwt.Workbook object
    """
    # initialise xlwt-stuff
    book = xlwt.Workbook()
    sheet = book.add_sheet('Bestillinger')

    # freeze first row and column
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(1)
    sheet.set_vert_split_pos(1)

    # method for writing to the sheet and updating column width
    def write_to_sheet(row, col, content):
        sheet.write(row, col, content)

        # if this content is the longest so far in this column,
        # update the column width
        length = len(str(content))
        if length > widths[col]:
            widths[col] = length
            # a character is roughly 256 'units' wide
            # we set the column width as the width of its longest text plus ~one char extra
            sheet.col(col).width = (256 * length) + 300

    # products that aren't kilt or sporran
    extras = Product.objects.filter(type=Product.EXTRA)

    # titles used in the excel sheet
    # if changes are made to column order, this must be changed too
    titles = [
        'Navn',
        'Kilt',
        'Størrelse',
        'Sporran',
        *extras.values_list('name', flat=True),
        'Kommentar'
    ]

    # list of column widths
    widths = [0] * len(titles)

    # writing titles to worksheet
    for i, title in enumerate(titles):
        write_to_sheet(0, i, title)

    period = OrderPeriod.objects.get(pk=pk)
    orders = period.orders.order_by('-user__gender', 'user__first_name', 'user__last_name')

    for i, order in enumerate(orders):
        # offset row by one due to titles in first row
        r = i + 1

        products = ProductInfo.objects.filter(order=order)

        kilt = products.filter(product__type=Product.KILT).first()
        if kilt:
            kilt_name = kilt.product.name
            kilt_size = kilt.size
        else:
            kilt_name = kilt_size = ''

        sporran = products.filter(product__type=Product.SPORRAN).first()
        sporran_name = sporran.product.name if sporran else ''

        num_extras = [''] * len(extras)
        for j, extra in enumerate(extras):
            info = products.filter(product=extra).first()
            num_extras[j] = info.number if info else ''

        write_to_sheet(r, 0, order.user.full_name)
        write_to_sheet(r, 1, kilt_name)
        write_to_sheet(r, 2, kilt_size)
        write_to_sheet(r, 3, sporran_name)
        for j, num in enumerate(num_extras):
            write_to_sheet(r, 4 + j, num)
        write_to_sheet(r, 4 + len(extras), order.comment)

    return book
