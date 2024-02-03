

# todo: Sync Process: reads multiple data types at the same time (when they're all available)

# todo: Batch process: reads all data of same type (with different data id) when they're all available

# if self.ismultiple:
#     d = self.datagroups[data.__DATAID__]
#     d.append((data, dtype))
#
#     # collect union data until all different types of same dataid are filled
#     if len(d) == len(self.consumes):
#         # todo: later: guarantee order of data union - the order of how they're listesd in .consumes
#         #              and handle same type occuring multiple times as well
#
#         resp = self.produce(*d)
#
#         del self.datagroups[data.__DATAID__]
# else:
# # for scalar data, just immediately process data
