#!/usr/bin/env bash
#
python3 get_minimal_binding.py Sigma_Zero/Sigma.spthy "Implicit_Key_Authentication_Initiator,SK_Authentication" &&
python3 get_minimal_binding.py Sigma_Zero/Sigma.spthy "Implicit_Key_Authentication_Initiator,SK_Authentication" --mal   
