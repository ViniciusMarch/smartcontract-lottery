from time import time
from brownie import network
import pytest
import time
from scripts.deploy_lottery import deploy_lottery

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    print("Deploying..")
    lottery = deploy_lottery()
    account = get_account()
    print("Starting the lottery..")
    lottery.startLottery({"from": account})
    print("Entering..")
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    print("Entering..")
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    print("Funding..")
    fund_with_link(lottery)
    print("Closing the lottery..")
    lottery.endLottery({"from": account})
    print("Waiting for the winner..")
    time.sleep(180)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
