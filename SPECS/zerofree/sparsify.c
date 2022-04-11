/*
 * sparsify - a tool to make files on an ext2 filesystem sparse
 *
 * Copyright (C) 2004-2012 R M Yorston
 *
 * This file may be redistributed under the terms of the GNU General Public
 * License, version 2.
 */
#include <ext2fs/ext2fs.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define USAGE "usage: %s [-n] [-v] filesystem filename ...\n"

/* initially assume pre-ext4 API version */
#define API 140

#if defined(BLOCK_FLAG_READ_ONLY)
#undef API
#define API 141
#endif

#if defined(EXT2_FLAG_64BITS)
#undef API
#define API 142
#endif

struct process_data {
	unsigned char *buf;
	int verbose;
	int dryrun;
	blk_t count;
	blk_t blocks;
	blk_t total_blocks;
	int old_percent;
};

static int process(ext2_filsys fs, blk_t *blocknr, e2_blkcnt_t blockcnt,
					blk_t ref_block, int ref_offset, void *priv)
{
	struct process_data *p;
	errcode_t errcode;
	int i, group;
	int ret = 0;

	p = (struct process_data *)priv;

	p->blocks++;
	if ( blockcnt >= 0 ) {
		errcode = io_channel_read_blk(fs->io, *blocknr, 1, p->buf);
		if ( errcode ) {
			return BLOCK_ABORT;
		}

		for ( i=0; i < fs->blocksize; ++i ) {
			if ( p->buf[i] ) {
				break;
			}
		}

		if ( i == fs->blocksize ) {
			p->count++;

			if ( !p->dryrun ) {
				ext2fs_unmark_block_bitmap(fs->block_map, *blocknr);
				group = ext2fs_group_of_blk(fs, *blocknr);
#if API >= 142
				ext2fs_bg_free_blocks_count_set(fs, group,
							ext2fs_bg_free_blocks_count(fs, group)+1);
				ext2fs_free_blocks_count_add(fs->super, (blk64_t)1);
#else
				fs->group_desc[group].bg_free_blocks_count++;
				fs->super->s_free_blocks_count++;
#endif
#if API >= 141
				ext2fs_group_desc_csum_set(fs, group);
#endif
				*blocknr = 0;
				ret = BLOCK_CHANGED;
			}
		}

		if ( p->verbose ) {
			double percent;

			percent = 100.0 * (double)p->blocks/(double)p->total_blocks;

			if ( (int)(percent*10) != p->old_percent ) {
				fprintf(stderr, "\r%4.1f%%", percent);
				p->old_percent = (int)(percent*10);
			}
		}
	}

	return ret;
}

int main(int argc, char **argv)
{
	int verbose = 0;
	int dryrun = 0;
	errcode_t ret;
	int flags;
	int superblock = 0;
	int open_flags = EXT2_FLAG_RW;
	int iter_flags = 0;
	int blocksize = 0;
	ext2_filsys fs = NULL;
	struct ext2_inode inode;
	ext2_ino_t root, cwd, inum;
	int i, c;
	struct process_data pdata;

	while ( (c=getopt(argc, argv, "nv")) != -1 ) {
		switch (c) {
		case 'n' :
			dryrun = 1;
#if defined(BLOCK_FLAG_READ_ONLY)
			iter_flags |= BLOCK_FLAG_READ_ONLY;
#endif
			break;
		case 'v' :
			verbose = 1;
			break;
		default :
			fprintf(stderr, USAGE, argv[0]);
			return 1;
		}
	}

	if ( argc < optind+2 ) {
		fprintf(stderr, USAGE, argv[0]);
		return 1;
	}

	ret = ext2fs_check_if_mounted(argv[optind], &flags);
	if ( ret ) {
		fprintf(stderr, "%s: failed to determine filesystem mount state  %s\n",
					argv[0], argv[optind]);
		return 1;
	}

	if ( flags & EXT2_MF_MOUNTED ) {
		fprintf(stderr, "%s: filesystem %s is mounted\n",
					argv[0], argv[optind]);
		return 1;
	}

	ret = ext2fs_open(argv[optind], open_flags, superblock, blocksize,
							unix_io_manager, &fs);
	if ( ret ) {
		fprintf(stderr, "%s: failed to open filesystem %s\n",
					argv[0], argv[optind]);
		return 1;
	}

	pdata.buf = (unsigned char *)malloc(fs->blocksize);
	if ( pdata.buf == NULL ) {
		fprintf(stderr, "%s: out of memory (surely not?)\n", argv[0]);
		return 1;
	}

	ret = ext2fs_read_inode_bitmap(fs);
	if ( ret ) {
		fprintf(stderr, "%s: error while reading inode bitmap\n", argv[0]);
		return 1;
	}

	ret = ext2fs_read_block_bitmap(fs);
	if ( ret ) {
		fprintf(stderr, "%s: error while reading block bitmap\n", argv[0]);
		return 1;
	}

	root = cwd = EXT2_ROOT_INO;

	for ( i=optind+1; i<argc; ++i ) {
		ret = ext2fs_namei(fs, root, cwd, argv[i], &inum);
		if ( ret ) {
			fprintf(stderr, "%s: failed to find file %s\n", argv[0], argv[i]);
			continue;
		}

		ret = ext2fs_read_inode(fs, inum, &inode);
		if ( ret ) {
			fprintf(stderr, "%s: failed to open inode %d\n", argv[0], inum);
			continue;
		}

		if ( !ext2fs_inode_has_valid_blocks(&inode) ) {
			fprintf(stderr, "%s: file %s has no valid blocks\n", argv[0],
					argv[i]);
			continue;
		}

#if defined(EXT4_EXTENTS_FL) && API < 141
		if ( inode.i_flags & EXT4_EXTENTS_FL ) {
			fprintf(stderr, "%s: unable to process %s, it uses extents\n",
					argv[0], argv[i]);
			continue;
		}
#endif

#if defined(EXT4_FEATURE_RO_COMPAT_HUGE_FILE) && defined(EXT4_HUGE_FILE_FL)
		if ( (fs->super->s_feature_ro_compat & EXT4_FEATURE_RO_COMPAT_HUGE_FILE)
				&& (inode.i_flags & EXT4_HUGE_FILE_FL) ) {
			fprintf(stderr, "%s: unable to process %s, it's huge\n",
					argv[0], argv[i]);
			continue;
		}
#endif

		if ( verbose ) {
			printf("processing %s\n", argv[i]);
		}

		pdata.verbose = verbose;
		pdata.dryrun = dryrun;
		pdata.count = pdata.blocks = 0;
		pdata.total_blocks = inode.i_blocks/(fs->blocksize >> 9);
		pdata.old_percent = 1000;
		ret = ext2fs_block_iterate2(fs, inum, iter_flags, NULL,
				process, &pdata);
		if ( ret ) {
			fprintf(stderr, "%s: failed to process file %s\n", argv[0],
					argv[i]);
			continue;
		}

		if ( pdata.count && !dryrun ) {
			ext2fs_mark_bb_dirty(fs);
			ext2fs_mark_super_dirty(fs);

			ret = ext2fs_read_inode(fs, inum, &inode);
			if ( ret ) {
				fprintf(stderr, "%s: failed to open inode (%s)\n", argv[0],
						argv[i]);
				continue;
			}

#if API >= 141
			ret = ext2fs_iblk_sub_blocks(fs, &inode, (blk64_t)pdata.count);
			if ( ret ) {
				fprintf(stderr, "%s: failed to update block count (%s)\n",
						argv[0], argv[i]);
				continue;
			}
#else
			inode.i_blocks -= pdata.count * (fs->blocksize >> 9);
#endif

			ret = ext2fs_write_inode(fs, inum, &inode);
			if ( ret ) {
				fprintf(stderr, "%s: failed to write inode (%s)\n",
						argv[0], argv[i]);
				continue;
			}
		}

		if ( verbose ) {
			printf("\r%d/%d/%d %s\n", pdata.count, pdata.blocks,
					pdata.total_blocks, argv[i]);
		}
	}

	ret = ext2fs_close(fs);
	if ( ret ) {
		fprintf(stderr, "%s: error while closing filesystem\n", argv[0]);
		return 1;
	}

	return 0;
}
