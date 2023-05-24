# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta
from itertools import chain


class ReportAccountAgedPartner(models.AbstractModel):
    _inherit = "account.aged.partner"

    @api.model
    def _get_query_period_table(self, options):
        def minus_days(date_obj, days):
            return fields.Date.to_string(date_obj - relativedelta(days=days))

        date_str = options['date']['date_to']
        date = fields.Date.from_string(date_str)
        period_values = [
            (False,                  date_str),
            (minus_days(date, 1),    minus_days(date, options['date']['interval'])),
            (minus_days(date, options['date']['interval']+1),   minus_days(date, options['date']['interval']+options['date']['interval2'])),
            (minus_days(date, (options['date']['interval']+options['date']['interval2'])+1),   minus_days(date, options['date']['interval']+options['date']['interval2']+options['date']['interval3'])),
            (minus_days(date, (options['date']['interval']+options['date']['interval2']+options['date']['interval3'])+1),   minus_days(date, options['date']['interval']+options['date']['interval2']+options['date']['interval3']+options['date']['interval4'])),
            (minus_days(date, (options['date']['interval']+options['date']['interval2']+options['date']['interval3']+options['date']['interval4'])+1),  False),
        ]

        period_table = ('(VALUES %s) AS period_table(date_start, date_stop, period_index)' %
                        ','.join("(%s, %s, %s)" for i, period in enumerate(period_values)))
        params = list(chain.from_iterable(
            (period[0] or None, period[1] or None, i)
            for i, period in enumerate(period_values)
        ))
        return self.env.cr.mogrify(period_table, params).decode(self.env.cr.connection.encoding)

    @api.model
    def _get_column_details(self, options):
        columns = [
            self._header_column(),
            self._field_column('report_date'),

            self._field_column('account_name', name=_("Account"), ellipsis=True),
            self._field_column('expected_pay_date'),
            self._field_column('period0', name=_("As of: %s", format_date(self.env, options['date']['date_to']))),
            self._field_column('period1', sortable=True, name=_("1 - %s", str(options['date']['interval']))),
            self._field_column('period2', sortable=True, name=_("%s - %s", str(options['date']['interval']+1), str(options['date']['interval']+options['date']['interval2']))),
            self._field_column('period3', sortable=True, name=_("%s - %s", str((options['date']['interval']+options['date']['interval2'])+1), str(options['date']['interval']+options['date']['interval2']+options['date']['interval3']))),
            # self._field_column('period4', sortable=True, name=_("%s - %s", str((options['date']['interval']*3)+1), str(options['date']['interval']*4))),
            self._field_column('period4', sortable=True, name=_("%s - %s", str((options['date']['interval'] +
                                                                                options['date']['interval2'] +
                                                                                options['date']['interval3']) + 1), str(
                options['date']['interval'] + options['date']['interval2'] + options['date']['interval3'] +
                options['date']['interval4']))),
            self._field_column('period5', sortable=True),
            self._custom_column(  # Avoid doing twice the sub-select in the view
                name=_('Total'),
                classes=['number'],
                formatter=self.format_value,
                getter=(
                    lambda v: v['period0'] + v['period1'] + v['period2'] + v['period3'] + v['period4'] + v['period5']),
                sortable=True,
            ),
        ]

        if self.user_has_groups('base.group_multi_currency'):
            columns[2:2] = [
                self._field_column('amount_currency'),
                self._field_column('currency_id'),
            ]
        return columns


class ReportAccountAgedReceivable(models.Model):
    _inherit = "account.aged.receivable"

    def _get_options(self, previous_options=None):
        # OVERRIDE
        options = super(ReportAccountAgedReceivable, self)._get_options(previous_options=previous_options)
        options['date'].update({
            'enable_interval': previous_options and previous_options.get('date') and previous_options['date'].get('enable_interval') or True,
            'interval': previous_options and previous_options.get('date') and previous_options['date'].get('interval') or 30,
            'interval2': previous_options and previous_options.get('date') and previous_options['date'].get(
                'interval2') or 30,
            'interval3': previous_options and previous_options.get('date') and previous_options['date'].get(
                'interval3') or 30,
            'interval4': previous_options and previous_options.get('date') and previous_options['date'].get(
                'interval4') or 30,
        })
        return options


class ReportAccountAgedPayable(models.Model):
    _inherit = "account.aged.payable"

    def _get_options(self, previous_options=None):
        # OVERRIDE
        options = super(ReportAccountAgedPayable, self)._get_options(previous_options=previous_options)
        options['date'].update({
            'enable_interval': previous_options and previous_options.get('date') and previous_options['date'].get(
                'enable_interval') or True,
            'interval': previous_options and previous_options.get('date') and previous_options['date'].get(
                'interval') or 30,
            'interval2': previous_options and previous_options.get('date') and previous_options['date'].get(
                'interval2') or 30,
            'interval3': previous_options and previous_options.get('date') and previous_options['date'].get(
                'interval3') or 30,
            'interval4': previous_options and previous_options.get('date') and previous_options['date'].get(
                'interval4') or 30,
        })
        return options
