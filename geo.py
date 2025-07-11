import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation
import datetime
from matplotlib.lines import Line2D

protest = gpd.read_file('event.shp')
events = pd.read_csv('event.csv')
hk = gpd.read_file('HKG_adm1.shp')
concat = protest.merge(events, on='event_id')
tg_points = gpd.read_file('tg_use_activist.shp')
tg_events = pd.read_csv('tg_use_activist.csv')
tg = tg_points.merge(tg_events, on='event_id')
stats = pd.read_csv('antielabdatastatistics.csv')

fig = plt.figure(figsize=(10, 10))
# protest.plot(ax=ax, alpha=0.7, color="red", zorder=5, markersize=2)
ax1 = fig.add_subplot(111)
ax2 = fig.add_subplot(333)


def animate(i):
    ax1.clear()
    ax2.clear()
    plt.title('Day-by-day visualisation of the 2019 Hong Kong protests', x=-0.6, y=1.1, fontsize='x-large')
    hk.plot(ax=ax1, color="grey", zorder=0, aspect=1)
    date = datetime.date(2019, 6, 12) + datetime.timedelta(days=i)
    date_str = date.strftime('%Y-%m-%d')
    events_daily = concat[concat['date'].str.contains(date_str)]
    assembly = events_daily[events_daily['type'].isin(['assembly', 'lunch', 'memorial'])]
    march = events_daily[events_daily['type'] == 'march']
    chain = events_daily[events_daily['type'] == 'wall']
    others = events_daily[events_daily['type'].isin(['others', 'screening', 'exhibition', 'market'])]
    assembly.plot(ax=ax1, alpha=0.5, marker='o', color="orange", zorder=5, markersize=50, aspect=1, legend=True)
    march.plot(ax=ax1, alpha=0.4, marker='o', color="red", zorder=5, markersize=50, aspect=1, legend=True)
    chain.plot(ax=ax1, alpha=0.4, marker='o', color="blue", zorder=5, markersize=50, aspect=1, legend=True)
    others.plot(ax=ax1, alpha=0.4, marker='o', color="green", zorder=5, markersize=50, aspect=1, legend=True)
    tg_daily = tg[tg['time_interval'].str.contains(date_str)]
    tg_daily.plot(ax=ax1, alpha=0.3, marker='s', color="black", zorder=4, markersize=60, aspect=1, legend=True)
    legend_elements = [Line2D([0], [0], marker='s', color='w', label='Tear Gas',
                              markerfacecolor='black', markersize=15),
                       Line2D([0], [0], marker='o', color='w', label='Assembly',
                              markerfacecolor='orange', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='March',
                              markerfacecolor='red', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Human Chain',
                              markerfacecolor='blue', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Other Protests',
                              markerfacecolor='green', markersize=10)
                       ]
    ax1.legend(handles=legend_elements, loc='lower right')
    ax1.text(113.9, 22.6, f'Date: {date_str}\nLive rounds fired: {stats["bullets_cumulative"].iloc[i + 4]}',
             fontsize='large')
    ax1.axis('off')
    stats_daily = stats[['Date', 'tg_cumulative', 'rubber_cumulative', 'bean_cumulative',
                         'sponge_cumulative']].iloc[3:i + 4]
    stats_daily.time = pd.to_datetime(stats_daily['Date'], format='%Y-%m-%d')
    stats_daily.set_index(['Date'], inplace=True)
    stats_daily.plot.line(ax=ax2)
    ax2.xaxis.set_tick_params(labelbottom=False)
    ax2.set_xticks([])
    ax2.set(xlabel=None)
    ax2.legend(loc='upper center', labels=['Tear gas rounds', 'Rubber bullets', 'Bean bag rounds', 'Sponge grenades'], bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=1)


ani = animation.FuncAnimation(fig, animate, interval=200)
# # writer = animation.FFMpegWriter(
# #       fps=15, metadata=dict(artist='Me'), bitrate=1800)
# # ani.save("movie.mp4", writer=writer)
plt.show()
