# -*- coding:utf-8 -*-
import re


def is_valid_email(addr):
    return re.match(r'[0-9A-Za-z\.]+@[a-z]+(.com)$', addr)


def name_of_email(addr):
    return re.match(r'(<?)([a-zA-Z\s]*)(>?)(\s?)([a-z]*)(@)([a-z]+)(.org)$', addr).group(2)


# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')

# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')