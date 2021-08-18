from django import template

register = template.Library()


def filter_child(model, args):
    dates = args.split(',')
    print(dates)
    startDate = dates[0]
    endDate = dates[1]
    return model.filter(journal__journalDate__range=[startDate, endDate])

register.filter('filter_child', filter_child)