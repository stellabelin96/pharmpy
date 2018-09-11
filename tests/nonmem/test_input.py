def test_data_io(nonmem, pheno_data):
    data_io = nonmem.input.NMTRANDataIO(pheno_data, '@')
    assert data_io.read(7) == '      1'
    data_io = nonmem.input.NMTRANDataIO(pheno_data, 'I')
    assert data_io.read(13) == '      1    0.'
    data_io = nonmem.input.NMTRANDataIO(pheno_data, 'Q')
    assert data_io.read(5) == 'ID TI'


def test_data_read(nonmem, pheno_real):
    model = nonmem.Model(pheno_real)
    df = model.input.data_frame
    assert list(df.iloc[1]) == [1.0, 2.0, 0.0, 1.4, 7.0, 17.3, 0.0, 0.0]
    assert list(df.columns) == ['ID', 'TIME', 'AMT', 'WGT', 'APGR', 'DV', 'FA1', 'FA2']

def test_input_filter(nonmem, pheno_real):
    model = nonmem.Model(pheno_real)
    filters = model.input.filters
