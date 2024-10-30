import streamlit as st
import vectorbt as vbt
from datetime import datetime

st.title('Crypto Statistical Arbitrage Backtest')

asset_1 = st.text_input('First Asset (e.g., BTC-USD)', 'BTC-USD')
asset_2 = st.text_input('Second Asset (e.g., ETH-USD)', 'ETH-USD')
timeframe = st.selectbox('Timeframe', ['1d'])
start_date = st.date_input('Start Date')
end_date = st.date_input('End Date')

start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

if st.button('Run Backtest'):
    try:
        data_1 = vbt.YFData.download(
            asset_1, start=start_date, end=end_date
        ).get('Close')

        data_2 = vbt.YFData.download(
            asset_2, start=start_date, end=end_date
        ).get('Close')

        spread = data_1 - data_2
        zscore = spread.vbt.zscore()

        long_entries = zscore < -1
        short_entries = zscore > 1
        exits = abs(zscore) < 0.5

        portfolio = vbt.Portfolio.from_signals(
            data_1, entries=long_entries, exits=exits,
            short_entries=short_entries, short_exits=exits, freq=timeframe, size=0.1
        )

        fig = portfolio.plot()
        st.plotly_chart(fig)

        st.subheader('Performance Metrics')
        st.write(portfolio.stats())

        st.subheader('Trades Stats')
        st.write(portfolio.trades.stats())

        st.subheader('Positions')
        st.write(portfolio.positions.records_readable)

        st.subheader('Drawdowns')
        st.write(portfolio.drawdowns.records_readable)

        st.subheader('Drawdown Plot')
        drawdown_fig = portfolio.drawdowns.plot()
        st.plotly_chart(drawdown_fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
