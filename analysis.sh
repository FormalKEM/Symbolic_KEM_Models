#!/usr/bin/env bash

if [ $1 = 'kyber' ] || [ $1 = 'all' ]
    then
    time python3 tamarin_wrapper.py Kyber/Kyber_AKE_EventBased_Model.spthy -t 3600 --resultfolder RES/results_kyber_no_flags
    time python3 tamarin_wrapper.py Kyber/Kyber_AKE_EventBased_Model.spthy -t 3600 -p "GoodKeysOnly" --resultfolder RES/results_kyber_hon
    time python3 tamarin_wrapper.py Kyber/Kyber_AKE_EventBased_Model.spthy -t 3600 -p "GoodKeysOnly,bindktoct,bindcttopk" --resultfolder RES/results_kyber_hon_full
    time python3 tamarin_wrapper.py Kyber/Kyber_AKE_EventBased_Model.spthy -t 3600 -p "MAL,bindktoct,bindcttopk,bindcttok" --resultfolder RES/results_kyber_mal
fi

if [ $1 = 'onepass' ] || [ $1 = 'all' ]
    then
    time python3 tamarin_wrapper.py OnepassAKE/OnepassAKE.spthy -t 3600 --resultfolder RES/results_onepass_no_flags
    time python3 tamarin_wrapper.py OnepassAKE/OnepassAKE.spthy -t 3600 -p "GoodKeysOnly" --resultfolder RES/results_onepass_hon
    time python3 tamarin_wrapper.py OnepassAKE/OnepassAKE.spthy -t 3600 -p "GoodKeysOnly,bindktoct,bindcttopk" --resultfolder RES/results_onepass_hon_full
    time python3 tamarin_wrapper.py OnepassAKE/OnepassAKE.spthy -t 3600 -p "MAL,bindktoct,bindcttopk,bindcttok" --resultfolder RES/results_onepass_mal
fi

if [ $1 = 'sigma' ] || [ $1 = 'all' ]
    then
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma.spthy -t 3600 --resultfolder RES/results_sigma_no_flags
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma.spthy -t 3600 -p "GoodKeysOnly" --resultfolder RES/results_sigma_hon
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma.spthy -t 3600 -p "GoodKeysOnly,bindktoct,bindcttopk" --resultfolder RES/results_sigma_hon_full
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma.spthy -t 3600 -p "MAL,bindktoct,bindcttopk,bindcttok" --resultfolder RES/results_sigma_mal
fi

if [ $1 = 'perfectsigma' ] || [ $1 = 'all' ]
    then
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma_Perfect.spthy -t 3600 --resultfolder RES/results_sigma_perfect_no_flags
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma_Perfect.spthy -t 3600 -p "GoodKeysOnly" --resultfolder RES/results_sigma_perfect_hon
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma_Perfect.spthy -t 3600 -p "GoodKeysOnly,bindktoct,bindcttopk" --resultfolder RES/results_sigma_perfect_hon_full
    time python3 tamarin_wrapper.py Sigma_Zero/Sigma_Perfect.spthy -t 3600 -p "MAL,bindktoct,bindcttopk,bindcttok" --resultfolder RES/results_sigma_perfect_mal
fi

if [ $1 = 'pqspdm' ] || [ $1 = 'all' ]
    then
    time python3 tamarin_wrapper.py PQSPDM/PQ_SPDM_AKE_EventBased_Model.spthy -t 3600 --resultfolder RES/results_spdm_no_flags
    time python3 tamarin_wrapper.py PQSPDM/PQ_SPDM_AKE_EventBased_Model.spthy -t 3600 -p "GoodKeysOnly" --resultfolder RES/results_spdm_hon
    time python3 tamarin_wrapper.py PQSPDM/PQ_SPDM_AKE_EventBased_Model.spthy -t 3600 -p "GoodKeysOnly,bindktoct,bindcttopk" --resultfolder RES/results_spdm_hon_full
    time python3 tamarin_wrapper.py PQSPDM/PQ_SPDM_AKE_EventBased_Model.spthy -t 3600 -p "MAL,bindktoct,bindcttopk,bindcttok" --resultfolder RES/results_spdm_mal
fi

