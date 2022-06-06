from dataclasses import dataclass, field

@dataclass(frozen=True)
class OneSampleMethylationData:
    file_name: str
    reads_number: int
    meth_patterns: list
    meth_levels: list[float]


@dataclass
class MethylationData:
    data: list[OneSampleMethylationData] = field(default_factory=list)
    
    def add(self, sample: OneSampleMethylationData):
        self.data.append(sample)


@dataclass(frozen=True)
class MethFlags:
    methylated_motif_flag = 1
    unmethylated_motif_flag = 0
    missing_motif_flag = "!"