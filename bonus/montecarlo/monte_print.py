import pandas as pd

def print_values(results):
    """Prints values for sim to terminal window
    Args:
        results (list[trial]): list of trials to calculate.
            Expect trial as [prior:str, posterior:str,win:boolean]
    """
    # generate df

    df = pd.DataFrame(results)
    df = df.rename(columns={0:"Prior", 1:"Posterior",2:"Result" })

    # abstract groupby calls

    prior_group = df.groupby("Prior")
    posterior_group = df.groupby(["Prior", "Posterior"])



    # Print distribution of Priors and Posteriors

    print("""
    Distribution of Prior Selections p(A)
    """)
    print(prior_group.count()["Result"])

    print("""
    Distribution of Posterior Selections p(A|B)
    Note, this is NOT the distribution of WINNING,
    only the rate at which each value is selected
    """)
    print(posterior_group.count()["Result"])



    # Print Wins, Losses, and Winning Rate

    print("""
    Data on wins
    """)

    winrate_series = df.groupby(["Result"]).count()["Posterior"]

    print(f"""
        Wins:{winrate_series[1]} 
        Losses: {winrate_series[0]} 
        Winrate: {winrate_series[1]/(winrate_series[1]+winrate_series[0])}
        """)

    # Wins by Prior
    
    print("""
    Wins by Prior Selection
    """)
    
    print(calculate_winrates(prior_group))

    # Wins by Posterior

    print("""
    Wins by Posterior Selection
    """)
    
    print(calculate_winrates(posterior_group))

def calculate_winrates(groupby_structure):
    """Generates Winrate column for prior and posterior group
    
    Args:
        groupby_structure(pandas.groupby)
    """

    win_df = groupby_structure.count().join(groupby_structure.sum(), rsuffix="win")
    win_df.rename(inplace=True, columns={"Result":"Trials", "Resultwin":"Wins"})
    win_df = win_df[["Trials","Wins"]]
    win_df["Winrate"] = win_df["Wins"]/win_df["Trials"]

    return win_df