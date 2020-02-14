if [ -z "$ARCH_DEFS_DIRECTORY" ]
then
    echo "ARCH_DEFS_DIRECTORY argument is empty! Please set it."
else
    export ARCH_DEFS_DIRECTORY=${1}
fi
