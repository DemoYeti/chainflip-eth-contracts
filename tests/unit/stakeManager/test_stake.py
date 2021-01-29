from consts import *
from shared_tests import *
from brownie import reverts
from brownie.test import given, strategy
from utils import *


# Hypothesis/brownie doesn't allow you to specifically include values when generating random
# inputs through @given, so this is a common fcn that can be used for `test_claim` and
# similar tests that test specific desired values
# Can't put the if conditions for `amount` in this fcn like in test_claim because
# it's we need to accomodate already having a tx because it's best to test
# `stakedMin` directly
def stakeTest(cf, tx, amount):
    # Check things that should've changed
    assert cf.flip.balanceOf(cf.stakeManager) == amount
    assert cf.stakeManager.getTotalStakeInFuture(0) == amount + getInflation(cf.stakeManager.tx.block_number, tx.block_number, EMISSION_PER_BLOCK)
    assert tx.events["Staked"][0].values() == [JUNK_INT, amount]
    # Check things that shouldn't have changed
    assert cf.stakeManager.getLastMintBlockNum() == cf.stakeManager.tx.block_number
    assert cf.stakeManager.getEmissionPerBlock() == EMISSION_PER_BLOCK
    assert cf.stakeManager.getMinimumStake() == MIN_STAKE


@given(amount=strategy('uint256', max_value=MAX_TEST_STAKE))
def test_stake(cf, amount):
    if amount < MIN_STAKE:
        with reverts(REV_MSG_MIN_STAKE):
            cf.stakeManager.stake(JUNK_INT, amount, {'from': cf.ALICE})
    else:
        tx = cf.stakeManager.stake(JUNK_INT, amount, {'from': cf.ALICE})
        stakeTest(cf, tx, amount)


def test_stake_min(cf, stakedMin):
    stakeTest(cf, *stakedMin)


def test_stake_rev_amount_just_under_minStake(cf):
    with reverts(REV_MSG_MIN_STAKE):
        cf.stakeManager.stake(JUNK_INT, MIN_STAKE-1, {'from': cf.ALICE})


def test_stake_rev_nodeID_nz(cf):
    with reverts(REV_MSG_NZ_UINT):
        cf.stakeManager.stake(0, cf.stakeManager.getMinimumStake(), {'from': cf.ALICE})


# Can't really test nofish since there's no known way to take FLIP
# out the contract
# def test_stake_rev_noFish(a, cf, stakedMin):
#     _, amount = stakedMin
#     NO_FISH = "StakeMan: small stake, peasant"

#     newAc = a.at(f'{cf.stakeManager.address}', force=True)
#     print(newAc)
#     a.add(newAc)

#     print(cf.stakeManager.address)
#     cf.flip.transfer(cf.DENICE, amount, {'from': a.at(f'{cf.stakeManager.address}', force=True)})
#     with reverts(NO_FISH):
#         cf.stakeManager.stake(JUNK_INT, MIN_STAKE, {'from': cf.ALICE})