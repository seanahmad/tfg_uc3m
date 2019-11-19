#!/bin/bash

usage() { echo "Usage: $0 -f <dataset main folder RELATIVE path>" 1>&2; exit 1; }

if [ "$#" -eq 0 ]
then
  usage
  exit 2
fi

while getopts "f:" o; do
    case "${o}" in
        f)
            dataset_folder=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${dataset_folder}" ]; then
    usage
fi

script_path="$(pwd)"

echo "Converting Lisa dataset from folder ${dataset_folder}"
cd "${dataset_folder}"

