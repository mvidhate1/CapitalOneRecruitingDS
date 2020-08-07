

def stratified_sample(df, strata, size=None, seed=None, keep_index=True):

    tmp_grpd = stratified_sample_report(df, strata, size)

    # controlling variable to create the dataframe or append to it
    first = True
    for i in range(len(tmp_grpd)):
        print('running')
        # query generator for each iteration
        qry = ''
        for s in range(len(strata)):
            stratum = strata[s]
            value = tmp_grpd.iloc[i][stratum]
            n = tmp_grpd.iloc[i]['samp_size']
            print(stratum)
            print(value)
            print(n)
            if type(value) == str:
                value = "'" + str(value) + "'"

            if s != len(strata) - 1:
                qry = qry + stratum + ' == ' + str(value) + ' & '
            else:
                qry = qry + stratum + ' == ' + str(value)

        print(qry)
        # final dataframe
        if first:
            stratified_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
            first = False
        else:
            tmp_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
            stratified_df = stratified_df.append(tmp_df, ignore_index=True)

    return stratified_df

def stratified_sample_report(df, strata, size=None):

    population = len(df)
    size = __smpl_size(population, size)
    tmp = df[strata]
    tmp.loc[:, 'size'] = 1
    print(tmp.head())
    tmp_grpd = tmp.groupby(strata).count().reset_index()
    print(tmp_grpd.head())
    tmp_grpd.loc[:, 'samp_size'] = round(size / population * tmp_grpd['size']).astype(int)

    return tmp_grpd

def __smpl_size(population, size):

    if size is None:
        cochran_n = round(((1.96) ** 2 * 0.5 * 0.5) / 0.05 ** 2)
        n = round(cochran_n / (1 + ((cochran_n - 1) / population)))
    elif size >= 0 and size < 1:
        n = round(population * size)
    elif size < 0:
        raise ValueError('Parameter "size" must be an integer or a proportion between 0 and 0.99.')
    elif size >= 1:
        n = size
    return n
