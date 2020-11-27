def checksum(string):
    """
    Compute the Luhn checksum for the provided string of digits. Note this
    assumes the check digit is in place.
    """
    digits = list(map(int, string))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10


def verify(string):
    """
    Check if the provided string of digits satisfies the Luhn checksum.

    >>> verify('356938035643809')
    True
    >>> verify('534618613411236')
    False
    """
    return (checksum(string) == 0)


def generate(string):
    """
    Generate the Luhn check digit to append to the provided string.

    >>> generate('35693803564380')
    9
    >>> generate('53461861341123')
    4
    """
    cksum = checksum(string + '0')
    return (10 - cksum) % 10


def append(string):
    """
    Append Luhn check digit to the end of the provided string.

    >>> append('53461861341123')
    '534618613411234'
    """
    return string + str(generate(string))





# var = "400000844943340"
# arr = list(var)
#
# digit_list = [int(i) for i in arr]
#
# helper = 0
#
# for i, num in enumerate(digit_list):
#     if i % 2 == 0:
#         if num * 2 > 9:
#             helper += num * 2 - 9
#         else:
#             helper += num * 2
#     else:
#         helper += num
#     result = 0 if helper % 10 == 0 else (helper // 10 + 1) * 10 - helper
