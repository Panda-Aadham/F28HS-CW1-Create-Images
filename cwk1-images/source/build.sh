#!/bin/sh -e
# Convert the source images into the appropriate formats.

# Check we're running from the right directory
[ -d source ]

convert () {
	infn="$1"
	outfn="$2"
	tempfn=/tmp/conv.ppm
	shift 2

	echo "Converting $infn -> $outfn"
	anytopnm <$infn >$tempfn
	hsconvert "$@" -f $fmt $tempfn $outfn

	echo "Checking $outfn"
	hsconvert $outfn $tempfn
}

for fmt in HS8 HS16 HSDEC HSHEX; do
	lfmt=$(echo $fmt | tr A-Z a-z)

	rm -fr $fmt
	mkdir $fmt

	for infn in source/*.png; do
		name=$(basename $infn .png)
		convert $infn $fmt/$name.$lfmt

		# Do randomised versions of some images
		case $name in
		pluge|redh|bars)
			convert $infn $fmt/$name.rand.$lfmt -r
			;;
		esac
	done
done
