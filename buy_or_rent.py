#!/usr/bin/env python
#
# Compare buying vs renting in terms of net worth, future liability, monthly
# payments, etc.
#
# Use at your own risk.
#
# (c) Jan Dlabal, 2017.
# http://houbysoft.com/
# Provided under the GNU GPL v3 License.

import matplotlib.pyplot as plt

# Edit these
RENT = {
    'monthly': 5000,
    'yearly_increase_percent': 3,
}

BUY = {
    'price': 1500000,
    'downpayment_percent': 20,
    'mortgage_percent': 4,
    'mortgage_years': 15,
    'appreciation_percent': 2,
}
# No need to edit anything after this line


def mortgage_monthly(params):
    """Calculate fixed monthly mortgage payment."""
    financed_amount = params['price'] * \
        ((100.0 - params['downpayment_percent']) / 100.0)
    monthly_interest_rate = (params['mortgage_percent']/100.0) / 12.0
    total_months = params['mortgage_years'] * 12.0
    return financed_amount * \
        ((monthly_interest_rate * (1.0+monthly_interest_rate)**total_months) / \
            ((1.0+monthly_interest_rate)**total_months - 1.0))


def rent_monthly(params, year):
    """Calculate monthly rent given the specified increases."""
    return params['monthly'] * ((100.0 + params['yearly_increase_percent']) / 100.0) ** year


def house_value(params, year):
    """Calculate total house value given the specified appreciation."""
    return params['price'] * ((100.0 + params['appreciation_percent']) / 100.0) ** year


def buy_net_worth(params, year):
    """Net worth at the beginning of given year if buying.

    + : House value and appreciation.
    - : All mortgage payments.
    - : Downpayment.
    """
    hv = house_value(params, year)
    fp = mortgage_monthly(params) * params['mortgage_years'] * 12
    return hv - fp - (params['downpayment_percent'] / 100.0) * params['price']


def buy_liability(params, year):
    """Liability at the beginning of given year if buying.

    + : House value and appreciation, less downpayment.
    - : Remaining mortgage payments.
    """
    hv = house_value(params, year) - (params['downpayment_percent'] / 100.0) * params['price']
    fp = mortgage_monthly(params) * (params['mortgage_years'] - year) * 12
    return min(hv - fp, 0)


def rent_net_worth(params, year):
    """Net worth at the beginning of given year if renting.

    - : All rent payments so far.
    """
    nw = 0
    for y in range(year):
        nw -= rent_monthly(params, y) * 12
    return nw


def stats(bp, rp):
    """Print out and show stats given the params.

    Args:
      bp: Buy parameters; see top of file for an example.
      rp: Rent parameters; see top of file for an example.
    """
    total_years = bp['mortgage_years']
    mortgage = mortgage_monthly(bp)
    
    years = range(total_years)
    buy_nets = []
    rent_nets = []
    buy_liabilities = []
    rents = []

    for year in years:
        rents.append(rent_monthly(rp, year))
        buy_nets.append(buy_net_worth(bp, year))
        rent_nets.append(rent_net_worth(rp, year))
        buy_liabilities.append(buy_liability(bp, year))
        print buy_liabilities[-1]
        print "Mortgage: $%.2f/mo\tRent: $%.2f/mo\tNet worth (buy): $%.2f\tNet worth (rent): $%.2f" % (mortgage, rents[-1], buy_nets[-1], rent_nets[-1])

    plt.figure(1)

    plt.subplot(211)
    plt.plot(years, buy_nets, label='Net worth (buy)')
    plt.plot(years, rent_nets, label='Net worth (rent)')
    plt.plot(years, buy_liabilities, label='Liability in case of sale (buy)')
    plt.plot(years, [0] * len(years), label='0')
    plt.xlabel('years')
    plt.ylabel('$')
    plt.title('Buy vs Rent')
    plt.legend(loc='lower left')

    plt.subplot(212)
    plt.plot(years, [mortgage] * len(years), label='Mortgage payment')
    plt.plot(years, rents, label='Rent payment')
    plt.xlabel('years')
    plt.ylabel('$ / mo')
    plt.title('Buy vs Rent Monthly')
    plt.legend(loc='lower left')
    plt.show()


def main():
    stats(BUY, RENT)


if __name__ == '__main__':
    main()
