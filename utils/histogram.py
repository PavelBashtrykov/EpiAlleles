import seaborn as sns


def generate_histogram(data, color="b"):
    sns.set_theme(style="ticks")
    sns.color_palette("Paired")
    sns.histplot(data=data, stat="probability", bins=10, color=color)
    # sns.despine()


def generate_histogram_kde(data, color="0.8"):
    ax = sns.histplot(
        data=data,
        stat="probability",
        bins=10,
        kde=True,
        color=color,
        kde_kws={"bw_adjust": 2},
    )
    ax.lines[0].set_color("crimson")
    # sns.despine()


def generate_histogram_2sets_1st(data, colors=["b", "g"]):
    sns.set_theme(style="ticks")
    sns.color_palette("Paired")
    sns.histplot(data=data[0], stat="probability", bins=10, color=colors[0])
    sns.histplot(data=data[1], stat="probability", bins=10, color=colors[1])


def generate_histogram_2sets(data):
    # sns.set_theme(style="ticks")
    # sns.color_palette("Paired")
    sns.color_palette()
    sns.histplot(
        data=data,
        x="meth_level",
        hue="sample",
        bins=10,
        stat="probability",
        common_norm=False,
        # multiple="stack",
        # kde=True,
    )

