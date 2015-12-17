import sys
import pstats

stats = pstats.Stats(sys.argv[1])
stats.sort_stats('cumulative')
stats.print_stats()
