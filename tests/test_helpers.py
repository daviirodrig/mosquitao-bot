from cmds.helpers.chanGet import main as chan


@pytest.mark.asyncio
async def test_chan():
    res = await chan()
    assert type(res) == list
    assert len(res) > 0
    assert type(res[0]) == str
    assert type(res[1]) == str



