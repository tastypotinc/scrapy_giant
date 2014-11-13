# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import numpy as np
import pylab as pl
import pytz
import matplotlib.pyplot as plt

from sklearn.hmm import GaussianHMM

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from bin.mongodb_driver import *
from bin.start import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report


class GaussianHmmLib(TradingAlgorithm):
    """
    ref: http://scikit-learn.org/0.14/auto_examples/applications/plot_hmm_stock_analysis.html
    """

    def __init__(self, dbquery, *args, **kwargs):
        super(GaussianHmmLib, self).__init__(*args, **kwargs)
        self.dbquery = dbquery
        self.mstockid = self.dbquery._stockmap.keys()[0]
        self.map = {
            'dates': np.array([]),
            'close_v': np.array([], dtype=float),
            'volume': np.array([], dtype=int)
        }
        self.hidden_states = None

#    def initialize(self):
#        self.invested = False
#
#    def handle_data(self, data):
#        self.map['dates'].append(data[self.mstockid].dt)
#        self.map['close_v'].append(data[self.mstockid].price)
#        self.map['volume'].append(data[self.mstockid].volume)
#
#    def post_run(self, n_components=5):
#        self.map['volume'] = self.map['volume'][1:]
#        diff = self.map['close_v'][1:] - self.map['close_v'][:-1]
#        X = np.column_stack([diff, self.map['volume']])
#        model = GaussianHMM(n_components, covariance_type="diag", n_iter=1000)
#        model.fit([X])
#        self.hidden_states = model.predict(X)


def main(debug=False, limit=0):
    proc = start_service(debug)
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        algname=GaussianHmmLib.__name__,
        sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)

    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit
    }
    for stockid in TwseIdDBQuery().get_stockids(**kwargs):
        dbquery = TwseHisDBQuery()
        data = dbquery.get_all_data(
            starttime=starttime, endtime=endtime,
            stockids=[stockid], traderids=[])
        if data.empty:
            continue
        hmm = GaussianHmmLib(dbquery=dbquery)
        hmm.run(data)
        hmm.post_run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test GaussianHmm algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    main(debug=True if args.debug else False, limit=args.limit)
