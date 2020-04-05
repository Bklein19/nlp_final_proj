import pandas as pd


def main():
    # getting facebook posts & ids
    cols = ['id', 'source', 'text']
    df = pd.read_csv('data/political_social_media.csv', usecols=cols, encoding='ISO-8859-1')
    df.query('source == "facebook"', inplace=True)
    df.drop('source', axis=1, inplace=True)
    df.rename(columns={'id': 'Id', 'text': 'Text'}, inplace=True)  # just to match the convention used in other files
    total_posts = len(df.index)

    # mapping facebook ids to twitter handles
    cols = ['facebook_id', 'twitter']
    handles_df = pd.read_csv('data/legislators-social-media.csv', usecols=cols, encoding='ISO-8859-1',
                             dtype={'facebook_id': object})
    handles = handles_df.set_index('facebook_id')['twitter'].to_dict()

    # mapping twitter handles to political parties
    parties_df = pd.read_csv('data/TwitterHandles.csv', encoding='ISO-8859-1')
    parties = parties_df.set_index('TwitterHandle')['Party'].to_dict()

    # getting the parties for each fb post
    df['Party'] = df['Id'].apply(lambda i: get_party(i, handles, parties))
    df.dropna(inplace=True)

    # just trying to figure out some stats about the data
    print('Party for {} posts could not be found'.format(total_posts - len(df.index)))
    num_reps = len(df.query('Party == "Republican"').index)
    num_dems = len(df.query('Party == "Democrat"').index)
    print('Republicans:', num_reps)
    print('Democrats:', num_dems)

    # generating final csv file
    with open('output/FacebookPosts.csv', 'w') as file:
        file.write(df.to_csv(index=False))


def get_party(fb_id, handles, parties):
    handle = get_handle(fb_id, handles)
    return parties.get(handle, None)


def get_handle(fb_id, handles):
    ids = fb_id.split('_')
    for i in ids:
        handle = handles.get(i, None)
        if handle is not None:
            return handle
    return None


if __name__ == '__main__':
    main()
