#!/usr/bin/env bash
#
python3 get_minimal_binding.py Kyber/Kyber_AKE_EventBased_Model.spthy "Implicit_Key_Authentication_Initiator,Implicit_Key_Authentication_Responder" &&
python3 get_minimal_binding.py Kyber/Kyber_AKE_EventBased_Model.spthy "Implicit_Key_Authentication_Initiator,Implicit_Key_Authentication_Responder" --mal   
