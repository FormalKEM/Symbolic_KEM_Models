#!/usr/bin/env bash
#
python3 get_minimal_binding.py OnepassAKE/OnepassAKE.spthy "ImplicitKeyAuthA" &&
python3 get_minimal_binding.py OnepassAKE/OnepassAKE.spthy "ImplicitKeyAuthA" --mal    
